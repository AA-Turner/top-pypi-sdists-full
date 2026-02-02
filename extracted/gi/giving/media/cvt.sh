
export NAME=$1

ffmpeg -i ${NAME}.mov -vf palettegen ${NAME}-palette.png
ffmpeg -i ${NAME}.mov -i ${NAME}-palette.png -lavfi paletteuse -r 5 ${NAME}.gif
