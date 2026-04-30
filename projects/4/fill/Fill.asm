// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(LOOP)
    // キーボード確認
    @KBD
    D=M
    @SET_WHITE
    D;JEQ

    // キーが押されたとき
    @color
    M=-1
    @FILL
    0;JMP

(SET_WHITE)
    @color
    M=0

(FILL)
    // addr = SCREEN
    @SCREEN
    D=A
    @addr
    M=D

(FILL_LOOP)
    // if(addr == KBD) goto LOOP
    @addr
    D=M
    @KBD
    D=D-A
    @LOOP
    D;JEQ

    // RAM[addr] = color
    @color
    D=M
    @addr
    A=M
    M=D

    // addr = addr + 1
    @addr
    M=M+1

    // goto FILL_LOOP
    @FILL_LOOP
    0;JMP