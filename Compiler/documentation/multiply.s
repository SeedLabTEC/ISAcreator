	.file	"multiply.c"
	.option nopic
	.text
	.align	1
	.globl	mult
	.type	mult, @function
mult:
	addi	sp,sp,-32
	sw	s0,28(sp)
	addi	s0,sp,32
	li	a5,5
	sw	a5,-20(s0)
	li	a5,3
	sw	a5,-24(s0)
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	mul	a5,a4,a5
	sw	a5,-28(s0)
	lw	a5,-28(s0)
	mv	a0,a5
	lw	s0,28(sp)
	addi	sp,sp,32
	jr	ra
	.size	mult, .-mult
	.ident	"GCC: (GNU) 8.2.0"
	.section	.note.GNU-stack,"",@progbits
