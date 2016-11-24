#!/bin/bash 
xterm -e "bash -c \"python Lsr A 2000 configA.txt; exec bash\"" & 
if false 
then 
xterm -e "bash -c \"python Lsr B 2001 configB.txt; exec bash\"" & 
xterm -e "bash -c \"python Lsr C 2002 configC.txt; exec bash\"" & 
xterm -e "bash -c \"python Lsr D 2003 configD.txt; exec bash\"" & 
xterm -e "bash -c \"python Lsr E 2004 configE.txt; exec bash\"" & 
xterm -e "bash -c \"python Lsr F 2005 configF.txt; exec bash\"" & 
fi