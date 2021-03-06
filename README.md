# gcc-bufdata-integrating2text
Integrating C Buffer Data Into the instruction of `.text` segment instead of on `.data`, `.rodata` to avoid copy.

# Usage

In your C code, invoke `INLINE_DATA_GEN(var_name, data)` 
and use this preprocessor to replace it.

Both `var_name` and `data` don't need quotation marks.
For detail, please check example.

# Example

Example in `test/`.

test.c:
```c
#include <stdio.h>
int main(){
    INLINE_DATA_GEN(buf, \x00\x01\x02aabbccjbinisdaf8wefwe322111hhh);
    printf(buf);
}
```

test_processed.c:
```c
#include <stdio.h>
int main(){
    __attribute__ ((aligned (1))) char
buf_32[] = {104},
buf_28[] = {49, 49, 104, 104},
buf_24[] = {51, 50, 50, 49},
buf_20[] = {101, 102, 119, 101},
buf_16[] = {97, 102, 56, 119},
buf_12[] = {110, 105, 115, 100},
buf_8[] = {99, 106, 98, 105},
buf_4[] = {97, 98, 98, 99},
buf_0[] = {0, 1, 2, 97}
;
char* buf = buf_0;
    printf(buf);
}
```

test_processed.s:
```asm
	.file	"test_processed.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movb	$104, -41(%rbp)
	movl	$1751658801, -40(%rbp)
	movl	$825373235, -36(%rbp)
	movl	$1702323813, -32(%rbp)
	movl	$2000184929, -28(%rbp)
	movl	$1685285230, -24(%rbp)
	movl	$1768057443, -20(%rbp)
	movl	$1667392097, -16(%rbp)
	movl	$1627521280, -12(%rbp)
	leaq	-12(%rbp), %rax
	movq	%rax, -56(%rbp)
	movq	-56(%rbp), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	xorq	%fs:40, %rdx
	je	.L3
	call	__stack_chk_fail@PLT
.L3:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:

```

It's easy to find that the buffer data aren't stored in the 
`.data` or `.rodata` segment.