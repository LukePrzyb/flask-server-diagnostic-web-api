#!/bin/bash

# a simple diagnostics system used to collect information about the server and transform it into
# a clean and simple format of information for a program to use 


results=$(free -m | tr -s ' ')

DELIMITHOLD=$IFS
IFS=$'\n'
results=($results)
IFS=$DELIMITHOLD

DETAILS=""

MEMORYDETAILS="MEMORY\n"

for (( i=0; i<${#results[@]}; i++ ))
do
	# echo "$i: ${results[$i]}"

	# Remove leading or trailing whitespace
	TEMP="$(echo -e ${results[$i]} | sed -e 's/^[[:space:]]*|[[:space:]]*$//')"

	if [ $i -eq 0 ]
	then
		IFS=$' '
		DETAILS=($TEMP)
		IFS=$DELIMITHOLD
	else

		IFS=$' '
		TEMP2=($TEMP)
		IFS=$DELIMITHOLD

		END="${TEMP2[0]}"

		for(( j=1; j<${#TEMP2[@]}; j++ ))
		do
			INTEG=$j-1
			END="$END${DETAILS[$INTEG]},${TEMP2[$j]}|"
		done

		# Trim trailing pipeline key at the end
		END=${END: : -1}

		# echo $END

		MEMORYDETAILS="$MEMORYDETAILS$END\n"
	fi
done

# Remove trailing new line
# MEMORYDETAILS=${MEMORYDETAILS: : -1}

echo -e $MEMORYDETAILS
echo ""

DETAILS=""
TEMP2=""

results=$(df -h | tr -s ' ' )

IFS=$'\n'
results=($results)
IFS=$DELIMITHOLD

FILESYSTEMDETAILS="FILESYSTEM\n"

for (( i=0; i<${#results[@]}; i++ ))
do
	TEMP="$(echo -e ${results[$i]} | sed -e 's/^[[:space:]]*|[[:space:]]*$//')"

	if [ $i -eq 0 ]
	then
		IF=$' '
		DETAILS=($TEMP)
		unset 'DETAILS[${#DETAILS[@]}-1]'
		IFS=$DELIMITHOLD
	else
		IFS=$' '
		TEMP2=($TEMP)
		IFS=$DELIMITHOLD

		END=""

		for(( j=0; j<${#TEMP2[@]}; j++ ))
		do
			END="$END${DETAILS[$j]},${TEMP2[$j]}|"
		done

		END=${END: : -1}

		FILESYSTEMDETAILS="$FILESYSTEMDETAILS$END\n"

	fi

done


echo -e $FILESYSTEMDETAILS
echo ""

