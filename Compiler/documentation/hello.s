	.text
	.file	"hello.c"
	.globl	main                    # -- Begin function main
	.p2align	3
	.type	main,@function
main:                                   # @main
# %bb.0:                                # %entry
	addi	sp, sp, -16
	sw	ra, 12(sp)
	sw	s0, 8(sp)
	addi	s0, sp, 16
	lui	a0, %hi(.L.str)
	addi	a0, a0, %lo(.L.str)
	lui	a1, %hi(printf)
	addi	a1, a1, %lo(printf)
	jalr	a1
	mv	a1, zero
	sw	a0, -12(s0)
	mv	a0, a1
	lw	s0, 8(sp)
	lw	ra, 12(sp)
	addi	sp, sp, 16
	ret
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
                                        # -- End function
	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"Hello World!\n"
	.size	.L.str, 14


	.ident	"clang version 7.0.0 (trunk 326957)"
	.section	".note.GNU-stack","",@progbits
