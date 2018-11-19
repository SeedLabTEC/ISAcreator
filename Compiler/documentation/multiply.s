	.text
	.file	"multiply.c"
	.globl	mult                    # -- Begin function mult
	.p2align	3
	.type	mult,@function
mult:                                   # @mult
# %bb.0:                                # %entry
	addi	sp, sp, -32
	sw	ra, 28(sp)
	sw	s0, 24(sp)
	addi	s0, sp, 32
	addi	a0, zero, 5
	sw	a0, -12(s0)
	addi	a0, zero, 3
	sw	a0, -16(s0)
	lw	a0, -12(s0)
	lw	a1, -16(s0)
	lui	a2, %hi(__mulsi3)
	addi	a2, a2, %lo(__mulsi3)
	jalr	a2
	sw	a0, -20(s0)
	lw	a0, -20(s0)
	lw	s0, 24(sp)
	lw	ra, 28(sp)
	addi	sp, sp, 32
	ret
.Lfunc_end0:
	.size	mult, .Lfunc_end0-mult
                                        # -- End function

	.ident	"clang version 7.0.0 (trunk 326957)"
	.section	".note.GNU-stack","",@progbits
