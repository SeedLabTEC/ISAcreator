touch ../Logs/TestBench.txt
touch ../Logs/CompileErrors.txt
iverilog  -o test -c list.txt 
vvp -l ../Logs/TestBench.txt test >/dev/null

