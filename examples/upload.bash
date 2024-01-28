
show_help()
{
cat << EOF

Usage: ./upload <script-name> 
Installs example script and library circuittpython device.  Note, library is installed in src subdirectory. 

-h      Shows this message 

EOF
}

while getopts ":h" option; do
    case $option in
        h)  show_help
            exit;;
    esac
done

echo 
echo "uploading example: " $1
echo "  " $1 "->" /media/$USER/CIRCUITPY
cp $1 /media/$USER/CIRCUITPY

echo 
echo "uploading library: " 
for entry in ../iorodeo_as7331/*
do
    echo "  " $entry "->" /media/$USER/CIRCUITPY/src
    mkdir -p /media/$USER/CIRCUITPY/src
    cp $entry /media/$USER/CIRCUITPY/src
done
echo

sync


