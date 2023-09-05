#!/bin/bash
echo 'updating kernel'
apt update
echo 'installing pip'
apt install python3-pip -y
echo 'installing pymysql'
pip install pymysql

echo 'Create database'
mysql -P9030 -h127.0.0.1 -uroot -e "
    create database test;
"

echo 'Create table transactions'
mysql -P9030 -h127.0.0.1 -uroot -e "
    use test;
    create table transactions(specversion integer NULL,baseWagerAmount integer NULL,customerWagerAmount integer NULL) distributed by hash(specversion) properties ('replication_num' = '1');
"
#create table transactions1( name1 STRING NOT NULL,specversion integer NULL,baseWagerAmount integer NULL,customerWagerAmount integer NULL) distributed by hash(name1) properties ('replication_num' = '1');
#insert into transactions1 values ("Brunos Mars",1,10,9);