#!/bin/bash
changeTags() {
    EDITOR_PATH='./dicomTagEditor'
    IN=$1
    OUT=${@: -1}
    
    # Separando Tags
    array=( "$@" )
    unset "array[${#array[@]}-1]"    # Removes last element
    unset "array[0]"    # Removes first element
    re='^[0-9]+$' # Para checar se parametro é um número ou não
    for i in "${array[@]}"; do
        if ! [[ $i =~ $re ]] ; then
            i="\"$i\""
        fi
        PARAMS="$PARAMS $i"
    done
    
    # Creating output directory
    if [ ! -d $OUT ]; then
        mkdir -p $OUT
    fi
    
    # Executando modificações
    for file in $IN/*.dcm; do
        filename=`basename $file`
        cmd="$EDITOR_PATH $file $PARAMS $OUT/$filename"
        echo $cmd
        eval $cmd
        echo
    done
}


#TO EDIT (não colocar nome dos arquivos!)
changeTags "`pwd`/SUBJ118_V3" 0010 0020 "IFD7851647" DO_UPLOAD_NEUROQUANT/SUBJ118_V3


# Outro exemplo
#changeTags "`pwd`/SUBJ124_V3" 0010 0010 "TESTE BRUNO" DO_UPLOAD_NEUROQUANT/