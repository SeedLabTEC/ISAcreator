## Creando un backend con LLVM para una arquitectura RISC-V 

[basado en cpu0 de Chen Chung-Shu](http://jonathan2251.github.io/lbd/about.html)

<p align="justify"> LLVM es una es una infraestructura para desarrollar compiladores, diseñada para optimizar el tiempo de enlazado, de compilación y de ejecución de cualquier lenguaje de programación definido por el usuario. </p>

<p align="justify"> Cuenta con una parte de frontend dónde se ingresa el código fuente, una segunda etapa de optimización y una final de backend en la que genera código máquina como se observa en la figura 1. </p>

<p align="center"> <img src="f1.png"> </p>

<p align="center"> Figura 1. Fases generales del compilador </p>

<p align="justify"> Debido a que el código de entrada puede ser cualquiera, es complejo el manejo de N posibles entradas. En este caso nos vamos a enfocar en el backend y el modelo intermedio (IR) que genera LLVM para la creación del código máquina deseado.</p>

### RISC-V

<p align="justify"> Primero se debe definir detalladamente la arquitectura del procesador a usar, en nuestro caso RISC-V se toma como base. En la figura 2 se describen algunas instrucciones en ensamblador de RISC-V.</p>

<p align="center"> <img src="f2.png"> </p>

<p align="center">Figura 2. Lenguaje ensamblador de RISC-V [Tomada del libro: "Computer Organization and Design The Hardware/Software Interface RISC-V Edition"]</p>

<p align="justify"> En la figura 3 se observan los principales formatos de instrucciones junto a su codificación. Es importante tener bien definidos los bits que le corresponden a cada parte de las instrucciones, más adelante se va a detallar cómo se agregan, modifican y eliminan los formatos de instrucciones en los archivos de configuración de LLVM. </p>

<p align="center"> <img src="f3.png"> </p>

<p align="center">Figura 3. RISC-V instruction formats [Tomada del libro: "Computer Organization and Design The Hardware/Software Interface RISC-V Edition"] </p>

<p align="justify"> En la figura 4 se observa la codificación de las instrucciones junto a los formatos descritos anteriormente, esta instrucciones al igual que en los formatos se agregan a los archivos de configuración de LLVM para su uso. </p>

<p align="center"> <img src="f4.png"> </p>

<p align="center">Figura 4. RISC-V instruction encoding [Tomada del libro: "Computer Organization and Design The Hardware/Software Interface RISC-V Edition"] </p>

<p align="justify"> RISC-V cuenta con 32 registros, los registros se deben describir en los archivos de configuración  de LLVM. </p>



### LLVM

<p align="justify"> Se va a trabajar sobre un compilador basado en <a href="https://github.com/riscv/riscv-llvm.git"> RISC-V de LLVM</a> , esto facilitará el trabajo de agregar casi 5000 líneas de código y se explicará cada uno de los archivos que se deben modificar para agregar o quitar destinos, modificar el ISA y la generación de código.</p>

#### Representación intermedia de LLVM (IR)

<p align="justify"> Uno de los aspecto más importante de su diseño del compilador es la representación intermedia de LLVM (IR), es la forma que utiliza para representar el código en el compilador. LLVM IR está diseñado para alojar análisis y transformaciones de nivel medio, se explica el <a href="http://releases.llvm.org/7.0.0/docs/CodeGenerator.html">capítulo de optimización de un compilador</a>. Fue diseñado con muchos objetivos específicos, incluyendo el soporte de optimizaciones de tiempo de ejecución, optimizaciones de funciones, análisis de todo el programa y transformaciones agresivas de reestructuración, etc. Sin embargo, el aspecto más importante de esto es que se define como un lenguaje de primera clase con semántica bien definida.  </p>

Un ejemplo simple de un archivo .ll :

```pseudocode
define i32 @add1(i32 %a, i32 %b) {
entry:
  %tmp1 = add i32 %a, %b
  ret i32 %tmp1
}
define i32 @add2(i32 %a, i32 %b) {
entry:
  %tmp1 = icmp eq i32 %a, 0
  br i1 %tmp1, label %done, label %recurse
recurse:
  %tmp2 = sub i32 %a, 1
  %tmp3 = add i32 %b, 1
  %tmp4 = call i32 @add2(i32 %tmp2, i32 %tmp3)
  ret i32 %tmp4
done:
  ret i32 %b
}
```

El código LLVM IR corresponde al código C siguiente:

```c
unsigned add1(unsigned a, unsigned b) {
  return a+b;
}
// Perhaps not the most efficient way to add two numbers.
unsigned add2(unsigned a, unsigned b) {
  if (a == 0) return b;
  return add2(a-1, b+1);
}
```

que proporciona dos formas diferentes de agregar números enteros.

<p align="justify"> Como se puede ver en este ejemplo, LLVM IR es un conjunto de instrucciones similar a RISC de bajo nivel. De la misma manera que en un conjunto de instrucciones RISC real, admite secuencias lineales de instrucciones simples como add, subtract, compare y branch. LLVM IR admite etiquetas, en general, parece una forma de lenguaje ensamblador.
</p>

<p align="justify"> A diferencia de la mayoría de los conjuntos de instrucciones RISC, LLVM está fuertemente tipado con un sistema de tipo simple (por ejemplo, i32 es un entero de 32 bits, i32** es un puntero a un entero de 32 bits) y algunos detalles de la máquina se abstraen. Por ejemplo, la convención de llamada se abstrae a través de instrucciones de llamada y retención, con argumentos explícitos. Otra diferencia significativa del código de máquina, es que LLVM IR no usa un conjunto fijo de registros con nombre, usa un conjunto infinito de nombres temporales con un carácter %. </p>

<p align="justify"> Más allá de ser implementado como un lenguaje, LLVM IR se define en realidad en tres formas isomórficas: el formato textual anterior, una estructura de datos en memoria inspeccionada y modificada por las optimizaciones en sí mismas, y un formato binario en disco. </p>

<p align="justify"> La representación intermedia de un compilador puede ser un "mundo perfecto" para el optimizador del compilador, a diferencia del frontend y el backend del compilador, el optimizador no está limitado por un idioma de origen específico o una máquina de destino específica . Tiene que hacerlo de la mejor manera para ambos casos, debe estar diseñado para que sea fácil de generar para el frontend y lo suficientemente expresivo como para permitir que se realicen importantes optimizaciones para objetivos reales. </p>



#### Archivos de descripción de destino de LLVM: .td

En los archivos .td de LLVM es dónde se describe el ISA y son procesados por la herramienta tblgen.

El idioma utilizado en los archivos .td es un lenguaje de descripción de destino (hardware) que permite a los ingenieros de compilación backend de llvm definir la transformación para LLVM IR y las instrucciones de la máquina de sus CPU. En la interfaz, las herramientas de desarrollo del compilador proporcionan el "parser generator" para el desarrollo del compilador; en el backend, proporcionan el generador de código de máquina para el desarrollo, tal como se muestra en la figura 5.

<p align="center"> <img src="f5.png"> </p>

<p align="center"> Figura 5. Descripción de la generación de código máquina en LLVM </p>

Los archivos que se deben modificar y/o crear .td son varios, se explicará cada uno de ellos con detalle.

La estructura destino está en target.td, que para este caso es RISCV.td

Este archivo está en el directorio lib/target y ahí es donde se encuentran todos los destinos a usar por el backend como x86, ARM, MIPS, PowerPC, etc. La carpeta lib está sobre el directorio en el cuál se va a trabajar, no es /lib del sistema operativo.

Dentro de .../target/ se encuentran varios archivos cmake y de construcción que usa LLVM para registrar un nuevo destino, específicamente en el archivo LLVMBuild.txt se debe ingresar en la sección de subdirectorio la carpeta del destino como RISCV o X86 por ejemplo.

```makefile
;===- ./lib/Target/LLVMBuild.txt -------------------------------*- Conf -*--===;
;
;                     The LLVM Compiler Infrastructure
;
; This file is distributed under the University of Illinois Open Source
; License. See LICENSE.TXT for details.
;
;===------------------------------------------------------------------------===;
;
; This is an LLVMBuild description file for the components in this subdirectory.
;
; For more information on the LLVMBuild system, please see:
;
;   http://llvm.org/docs/LLVMBuild.html
;
;===------------------------------------------------------------------------===;

; Please keep these as one per line so that out-of-tree merges
; will typically require only insertion of a line.
[common]
subdirectories =
 RISCV
 X86
 NewTarget
 ...

```

Dentro de .../target/RISCV que será el directorio a trabajar se encuentran todos los archivos .td que se deben modificar.

En el archivo RISCV.td se define la interfaz SubtargetFeature, donde los primeros 4 parámetros de cadena de la interfaz son un nombre de característica, un atributo establecido por la característica, el valor del atributo y una descripción de la característica.

```makefile
...
def FeatureDr  : SubtargetFeature<"dr", "HasDR", "true","Tardis">;
...
```

Es RISCV.td se incluye a Target.td que es de LLVM, se agregan también los nombres de los archivos que van a contener la descripción de las instrucciones, los registros, el generador de ensamblador y la interfaz SubtargetFeature.

```makefile
//===-- RISCV.td - Describe the RISCV target machine ---------*- tblgen -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

//===----------------------------------------------------------------------===//
// Target-independent interfaces which we are implementing
//===----------------------------------------------------------------------===//

include "llvm/Target/Target.td"

//===----------------------------------------------------------------------===//
// RISCV subtarget features
//===----------------------------------------------------------------------===//

def FeatureM : SubtargetFeature<"m", "HasM", "true",
                                "Supports Integer Multiplication and Division.">;
def FeatureA : SubtargetFeature<"a", "HasA", "true",
                                "Supports Atomic Instructions.">;
```

En RISCVInstrInfo.td se describen las instrucciones de propósito general como add, stl, sub; en cada instrucción se debe definir el nombre, el formato, los bits para cada parte según se definió en el ISA al inicio.

```makefile
/*******************
*RISCV Instructions
********************/
//Integer arithmetic register-register
def ADD : InstR<"add" , 0b0110011, 0b0000000, 0b000, add   , GR32, GR32>;
def SLT : InstR<"slt" , 0b0110011, 0b0000000, 0b010, setlt , GR32, GR32>;
def SLTU: InstR<"sltu", 0b0110011, 0b0000000, 0b011, setult, GR32, GR32>;
def XOR : InstR<"xor" , 0b0110011, 0b0000000, 0b100, xor   , GR32, GR32>;
def OR  : InstR<"or"  , 0b0110011, 0b0000000, 0b110, or    , GR32, GR32>;
def AND : InstR<"and" , 0b0110011, 0b0000000, 0b111, and   , GR32, GR32>;
//Integer arithmetic register-immediate
def XORI: InstI<"xori", 0b0010011, 0b100       , xor, GR32, GR32, imm32sx12>;
def ORI : InstI<"ori" , 0b0010011, 0b110       , or , GR32, GR32, imm32sx12>;
def ANDI: InstI<"andi", 0b0010011, 0b111       , and, GR32, GR32, imm32sx12>;
```

En RISCVInstrFormats.td se definen los formatos de las instrucciones.

```makefile
//===----------------------------------------------------------------------===//
// Basic RISCV instruction definition
//===----------------------------------------------------------------------===//

class InstRISCV<int size, dag outs, dag ins, string asmstr,
                  list<dag> pattern> : Instruction {
  let Namespace = "RISCV";

  dag OutOperandList = outs;
  dag InOperandList = ins;
  let Size = size;
  let Pattern = pattern;
  let AsmString = asmstr;

  let AddedComplexity = 1;

  // Used to identify a group of related instructions, such as ST and STY.
  string Function = "";

  // "12" for an instruction that has a ...Y equivalent, "20" for that
  // ...Y equivalent.
  string PairType = "none";

  // True if this instruction is a simple load of a register
  // (with no sign or zero extension).
  bit SimpleLoad = 0;

  // True if this instruction is a simple store of a register
  // (with no truncation).
  bit SimpleStore = 0;

  let TSFlags{0} = SimpleLoad;
  let TSFlags{1} = SimpleStore;
}

```

Como ejemplo se describe el formato R, se describen los bits del código de operación, los bits de funct3 y funct7, así como los registros operadores tal y como se había analizado en la figura 3

```makefile
//R-Type
class InstR<string mnemonic, bits<7> op, bits<7> funct7, bits<3> funct3,
            SDPatternOperator operator, RegisterOperand cls1, 
            RegisterOperand cls2>
  : InstRISCV<4, (outs cls1:$dst), (ins cls2:$src1, cls2:$src2),
                mnemonic#"\t$dst, $src1, $src2", 
                [(set cls1:$dst, (operator cls2:$src1, cls2:$src2))]> {
  field bits<32> Inst;

  bits<5> RD;
  bits<5> RS1;
  bits<5> RS2;

  let Inst{31-25} = funct7;
  let Inst{24-20} = RS2;
  let Inst{19-15} = RS1;
  let Inst{14-12} = funct3;
  let Inst{11- 7} = RD;
  let Inst{6 - 0} = op;
}
```





#### Secuencia de generación de código de LLVM

<p align="center"> <img src="f6.png"> </p>

<p align="center"> Figura 6. Secuencia de generación de código.</p>

En la ruta del código LLVM al código ensamblador, se ejecutan numerosos pases y se utilizan varias estructuras de datos para representar los resultados intermedios.

LLVM es una representación basada en asignación estática única en inglés Static Single Assignment (SSA). LLVM proporciona un número infinito de registros virtuales tal como se mencionó anteriormente, pueden contener valores de tipo primitivo (integral, de punto flotante o de puntero). Por lo tanto, cada operando se puede guardar en un registro virtual diferente en la representación SSA de LLVM. Los comentarios se representan con ";".  Un ejemplo de la representación es:

```pseudocode
store i32 0, i32* %a  ; store i32 type of 0 to virtual register %a, %a is
            ;  pointer type which point to i32 value
store i32 %b, i32* %c ; store %b contents to %c point to, %b isi32 type virtual
            ;  register, %c is pointer type which point to i32 value.
%a1 = load i32* %a    ; load the memory value where %a point to and assign the
            ;  memory value to %a1
%a3 = add i32 %a2, 1  ; add %a2 and 1 and save to %a3
```

