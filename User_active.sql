SELECT DISTINCT u.id as ID,u.lower_user_name as lower_username, u.lower_email_address as email
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 5.6/Uploads/users_active.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\r\n'
FROM   cwd_user u 
       JOIN cwd_membership m 
         ON u.id = m.child_id 
            AND u.directory_id = m.directory_id 
       JOIN schemepermissions sp 
         ON Lower(m.parent_name) = Lower(sp.perm_parameter) 
       JOIN cwd_directory d 
         ON m.directory_id = d.id 
WHERE  sp.permission IN ( '0', '1', '44' ) 
       AND d.active = '1' 
       AND u.active = '1';

