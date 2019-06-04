#!/bin/bash

source ~/.bashrc
allure_dir=$(dirname $(readlink -f $0))"/allure/bin"
echo 'allure_dir -      '$allure_dir
allure=$(dirname $(readlink -f $0))"/allure/bin/allure"
echo 'allure -          '$allure
allure_report=$(dirname $(readlink -f $0))"/allure-report"
echo 'allure_report -   '$allure_report
generatedReport=$(dirname $(readlink -f $0))"/generatedReport"
echo 'generatedReport - '$generatedReport

if [ -d $allure_dir ]; then
    export ALLURE_NO_ANALYTICS=1
    if [ ! -d $allure_report ]; then
        mkdir -p $allure_report
        echo 'allure-report folder have been created'
    fi
    if [ ! -d $generatedReport ]; then
        mkdir -p $generatedReport
        echo 'generatedReport folder have been created'
    fi
    pytest --alluredir=generatedReport -n 4 -s -v --tb=line --continue-on-collection-errors --cache-clear --durations=5 --clean-alluredir
    cp ./cfg/categories.json ./generatedReport/
    $allure generate --clean ./generatedReport/ --output $allure_report
    wait
    if [ -d $generatedReport ]; then
        rm -rf $generatedReport && mkdir $generatedReport
        echo 'generatedReport have been cleared - '$generatedReport
    fi
else
    echo "Please place $allure_ver directory inside $PWD"
    exit
fi
