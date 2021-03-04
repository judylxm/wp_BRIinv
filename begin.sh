wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum makecache
yum update 
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm
sudo yum install mysql-server
service mysqld start
wget http://gosspublic.alicdn.com/ossutil/1.6.14/ossutil64
chmod 755 ossutil64
./ossutil64 config



# mysql -u root -p
# use mysql;
# update user set password=password('123456') where user='root';
# exit;
# service mysqld restart
# mysqldump -u root -p hikki > hikki.sql