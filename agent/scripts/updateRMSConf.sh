#!/bin/sh
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

#------------------------------------------------------------------------------------------------------
# Tool Usage
#------------------------------------------------------------------------------------------------------
usage()
{
    echo -e "\nUsage : sh updateRMSConfig.sh [action] "
    echo -e "Eg    : sh $0 \"configure\" "
    echo -e "                  or        "
    echo -e "      : sh $0 \"revert\"\n"
}


#------------------------------------------------------------------------------------------------------
# Checking Command Line Arguments
#------------------------------------------------------------------------------------------------------
ACTION=""
argument_count=$#
if [[ $argument_count -gt 0 ]]; then
    ACTION="$1"
else
    usage
    exit 0
fi

#------------------------------------------------------------------------------------------------------
# Update RMS Configurations
#------------------------------------------------------------------------------------------------------

RMS_CONF="/usr/local/rms/bin/rms.conf"
RMS_CONFIG="/usr/local/rms/config/config.lua"
RMS_CONF_BACKUP="/opt/TDK/backup_rms.conf"
RMS_CONFIG_BACKUP="/opt/TDK/backup_rms_config.lua"
if [[ $ACTION == "configure" ]]; then

    if [[ -f $RMS_CONF ]]; then
        echo -e "Checking resolution configurations in $RMS_CONF ...."
        rm -rf $RMS_CONF_BACKUP > /dev/null 2>&1
        cp $RMS_CONF $RMS_CONF_BACKUP
        if [[ $? -eq 0 ]]; then
            echo -e "Taking backup : copied $RMS_CONF to $RMS_CONF_BACKUP"
        else
            echo -e "Taking backup : copy $RMS_CONF to $RMS_CONF_BACKUP failed"
        fi
        rms_conf_update=0
        width=$(awk '/WIDTH=*/ {print $0}' $RMS_CONF)
        height=$(awk '/HEIGHT=*/ {print $0}' $RMS_CONF)
        if [[ ! -z $width && ! -z $height ]]; then
            echo -e "Existing $width , $height"
            width=$(echo $width | cut -d "=" -f 2)
            height=$(echo $height | cut -d "=" -f 2)
            if [[ $width -eq 1280 && $height -eq 720 ]]; then
                echo -e "Resolution details are present already"
            else
                rms_conf_update=1
                echo -e "over-writing resolution info in $RMS_CONF"
                sed -i -E 's/WIDTH=.+/WIDTH=1280/' $RMS_CONF
                sed -i -E 's/HEIGHT=.+/HEIGHT=/720' $RMS_CONF
            fi
        else
            rms_conf_update=1
            echo -e "writing resolution info in $RMS_CONF"
            echo "WIDTH=1280" >> $RMS_CONF
            echo "HEIGHT=720" >> $RMS_CONF
        fi
        if [[ ! -z $2 && $2 != " " ]]; then
            echo -e "Updating Room ID in $RMS_CONF ..."
            room_id=$(awk '/ROOMID=*/ {print $0}' $RMS_CONF | cut -d "=" -f 2)
            echo -e "Existing Room ID : $room_id"
            if [[ $room_id == $2 ]];then
                echo -e "Required Room ID present already"
            else
                rms_conf_update=1
                echo -e "over-writing Room ID info in $RMS_CONF"
                sed -i -E 's/ROOMID=.+/ROOMID='"$2"'/' $RMS_CONF
            fi
        fi
        echo -e "\nCurrent data in $RMS_CONF:"
        cat $RMS_CONF
        if [[ $rms_conf_update == 0 ]];then
            rm -rf $RMS_CONF_BACKUP > /dev/null 2>&1
        fi

    else
        echo -e "File $RMS_CONF not Found\n"
        exit 0
    fi

    if [[ -f $RMS_CONFIG ]]; then
        rm -rf $RMS_CONFIG_BACKUP > /dev/null 2>&1
        logging_line_no=$(awk '/name=\"file appender\"/{print NR":"$0}' $RMS_CONFIG | cut -d ":" -f 1)
        start_line_no=`expr $logging_line_no - 1`
        logging_section=$(sed -n ''"$start_line_no"','"$start_line_no"'p' $RMS_CONFIG)
        if [[ "$logging_section" == *"--[["* ]]; then
            echo -e "\nUncommenting file appender section in $RMS_CONFIG ..."
            cp $RMS_CONFIG $RMS_CONFIG_BACKUP
            if [[ $? -eq 0 ]]; then
                echo -e "Taking backup : copied $RMS_CONFIG to $RMS_CONFIG_BACKUP"
            else
                echo -e "Taking backup : copy $RMS_CONFIG to $RMS_CONFIG_BACKUP failed"
            fi
            #sed -n ''"$start_line_no"',/\}*\]\]--/p' $RMS_CONFIG
            total_line_no=$(sed -n ''"$start_line_no"',/\}*\]\]--/p' $RMS_CONFIG | wc -l)
            end_line_no=`expr $start_line_no + $total_line_no - 1`
            sed -i ''"$start_line_no"'s/--\[\[//' $RMS_CONFIG
            sed -i ''"$end_line_no"'s/\]\]--//'   $RMS_CONFIG
            #echo -e "\nSection after uncommenting: "
            #sed -n "${start_line_no},${end_line_no}p" $RMS_CONFIG
        else
            echo -e "\nfile appender section in $RMS_CONFIG is already uncommented"
        fi
    else
        echo -e "File $RMS_CONF not Found\n"
        exit 0
    fi
    rm -rf /opt/logs/rms.*.log > /dev/null 2>&1

elif [[ $ACTION == "revert" ]]; then
    if [[ -f $RMS_CONF_BACKUP ]]; then
        if [[ -f $RMS_CONF ]]; then
            cp $RMS_CONF_BACKUP $RMS_CONF
            if [[ $? -eq 0 ]]; then
                echo -e "$RMS_CONFIG configurations reverted successfully"
                echo -e "Current data in $RMS_CONF:"
                cat $RMS_CONF
            else
                echo -e "$RMS_CONF file configurations revert failed"
            fi
        else
            echo "$RMS_CONF file not found to revert the configurations"
        fi
    else
        echo "$RMS_CONF configurations remains same"
    fi

    if [[ -f $RMS_CONFIG_BACKUP ]]; then
        if [[ -f $RMS_CONFIG ]]; then
            cp $RMS_CONFIG_BACKUP $RMS_CONFIG
            if [[ $? -eq 0 ]]; then
                echo -e "\nFile append configurations in $RMS_CONFIG reverted successfully"
                #echo -e "Section after commenting :"
                #logging_line_no=$(awk '/name=\"file appender\"/{print NR":"$0}' $RMS_CONFIG | cut -d ":" -f 1)
                #start_line_no=`expr $logging_line_no - 1`
                #sed -n ''"$start_line_no"',/\}*\]\]--/p' $RMS_CONFIG
            else
                echo -e "$RMS_CONFIG file append configurations revert failed"
            fi
        else
            echo "$RMS_CONFIG file not found to revert the file append configurations"
        fi
    else
        echo "File append configurations in $RMS_CONFIG remains same"
    fi
fi

