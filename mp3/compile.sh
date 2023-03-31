#!/bin/bash

COMP="javac"
BITCOINLIB="./libs/api-1.2.0.jar"
JSON="./libs/gson-2.2.jar"
LANG="./libs/commons-lang3-3.12.0.jar"
CLASSPATH=".:$BITCOINLIB:$JSON:$LANG"
OUTDIR="./bin"

EXTRA=""

FILES="src/main/*.java src/test/*.java"

mkdir "$OUTDIR" 2> /dev/null

cmd=`echo "$COMP" "$EXTRA" -classpath "$CLASSPATH" -d "$OUTDIR" "$FILES"`
echo "Compilation command: \"$cmd\" ";

echo "-------------------------------"

$cmd

if [ $? -eq 0 ]; then
	echo "Compilation succeeded!";
else
	echo "Compilation failed!";
fi
