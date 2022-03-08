#!/bin/bash

FILES=(
    'instances/i01'
    'instances/i02'
    'instances/i03'
    'instances/i04'
    'instances/i05'
    'instances/i06'
    'instances/i07'
    'instances/i08'
    'instances/i09'
    'instances/i10'
)

# FILES=(
#     'instances/i01'
# )

for i in "${FILES[@]}"; do
    echo "-----------------------------------------"
    echo "$i"
    echo "-----------------------------------------"
    ulimit -v 3000000
    timeout 180s python3 pagecollect.py "$i" || echo "Timeout"
    echo "-----------------------------------------"
    echo ""
done
