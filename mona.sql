create table replies(id integer primary key autoincrement, keyword varchar(100), reply varchar(100));
create index keyword_index on replies(keyword);
insert into replies (keyword, reply) values ("sony", "大法好");
insert into replies (keyword, reply) values ("启动", "P5R天下第一");
insert into replies (keyword, reply) values ("合理", "好几百个教授一致通过");