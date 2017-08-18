use jiradb;

DROP TABLE IF EXISTS usermigration;

create table usermigration
(
oldusername varchar(255),
newusername varchar(255)
);

/*
insert into usermigration (oldusername, newusername) values ('felix henon',lower('soft_poly'));
insert into usermigration (oldusername, newusername) values ('ikhediri',lower('ines.khedhiri'));
insert into usermigration (oldusername, newusername) values ('integration',lower('Rodolph.Riou'));
*/
insert into usermigration (oldusername, newusername) values ('rriou',lower('Rodolph.Riou'));
insert into usermigration (oldusername, newusername) values ('ikhedhiri',lower('ines.khedhiri'));

insert into usermigration (oldusername, newusername) values ('ael-harraq',lower('Abderrazak.El-Harraq'));
insert into usermigration (oldusername, newusername) values ('adrien.fortune',lower('adrien.fortune'));
insert into usermigration (oldusername, newusername) values ('afortune',lower('adrien.fortune'));
insert into usermigration (oldusername, newusername) values ('aviala',lower('Adrien.Viala'));
insert into usermigration (oldusername, newusername) values ('anedelle',lower('Alain.Nedellec'));
insert into usermigration (oldusername, newusername) values ('arosal',lower('Albert.Rosal'));
insert into usermigration (oldusername, newusername) values ('asamimi',lower('Ali.Samimi'));
insert into usermigration (oldusername, newusername) values ('atrela',lower('Andre.Trela'));
insert into usermigration (oldusername, newusername) values ('aoutrey',lower('Armelle.Outrey'));
insert into usermigration (oldusername, newusername) values ('adelhors',lower('arnaud.delhors'));
insert into usermigration (oldusername, newusername) values ('apouyadou',lower('Arnaud.Pouyadou'));
insert into usermigration (oldusername, newusername) values ('acollet',lower('Aurelien.Collet'));
insert into usermigration (oldusername, newusername) values ('baabelka',lower('B.Ait-Ali-Belkacem'));
insert into usermigration (oldusername, newusername) values ('briquet',lower('b.riquet'));
insert into usermigration (oldusername, newusername) values ('bderouin',lower('Bastien.Derouineau'));
insert into usermigration (oldusername, newusername) values ('bsaraiva',lower('Bertrand.Saraiva'));
insert into usermigration (oldusername, newusername) values ('bpanloup',lower('boris.panloup'));
insert into usermigration (oldusername, newusername) values ('bkarmouc',lower('Brahim.Karmouche'));
insert into usermigration (oldusername, newusername) values ('brolet',lower('Bruno.Rolet'));
insert into usermigration (oldusername, newusername) values ('cdsantos',lower('C.Dos-Santos'));
insert into usermigration (oldusername, newusername) values ('cfleurentin',lower('c.fleurentin'));
insert into usermigration (oldusername, newusername) values ('cdelacru',lower('Carlos.De-La-Cruz'));
insert into usermigration (oldusername, newusername) values ('cjeanney',lower('Christine.Jeanney'));
insert into usermigration (oldusername, newusername) values ('cbellan',lower('Christophe.Bellan'));
insert into usermigration (oldusername, newusername) values ('cgendraud',lower('Christophe.Gendraud'));
insert into usermigration (oldusername, newusername) values ('ddouillard',lower('Daniel.Douillard'));
insert into usermigration (oldusername, newusername) values ('echevalier',lower('Elisabeth.Chevalier'));
insert into usermigration (oldusername, newusername) values ('ebervas',lower('Elodie.Bervas'));
insert into usermigration (oldusername, newusername) values ('ebaillie',lower('Emmanuel.Baillie'));
insert into usermigration (oldusername, newusername) values ('EAPFELSTAEDT',lower('Enrico.Apfelstaedt'));
insert into usermigration (oldusername, newusername) values ('epizard',lower('Eric.Izard'));
insert into usermigration (oldusername, newusername) values ('equero',lower('Eric.Quero'));
insert into usermigration (oldusername, newusername) values ('edelaplace',lower('Etienne.Delaplace'));
insert into usermigration (oldusername, newusername) values ('frouvery',lower('Fabien.Rouvery'));
insert into usermigration (oldusername, newusername) values ('fbenbekhti',lower('farid.benbekhti'));
insert into usermigration (oldusername, newusername) values ('fbeaufrere',lower('Florence.Beaufrere'));
insert into usermigration (oldusername, newusername) values ('fbigot',lower('Francois.Bigot'));
insert into usermigration (oldusername, newusername) values ('fperrein',lower('Francois.Perrein'));
insert into usermigration (oldusername, newusername) values ('fbaudemont',lower('Frederic.Baudemont'));
insert into usermigration (oldusername, newusername) values ('ffraslin',lower('Frederic.Fraslin'));
insert into usermigration (oldusername, newusername) values ('gcasse',lower('Gilles.Casse'));
insert into usermigration (oldusername, newusername) values ('ggrossi',lower('Gregory.Grossi'));
insert into usermigration (oldusername, newusername) values ('gbazat',lower('Guillaume.Bazat'));
insert into usermigration (oldusername, newusername) values ('gpernot',lower('Guillaume.Pernot'));
insert into usermigration (oldusername, newusername) values ('hsedjane',lower('hamid.sedjane'));
insert into usermigration (oldusername, newusername) values ('hchouket',lower('Houda.Chouket'));
insert into usermigration (oldusername, newusername) values ('houda.chouket',lower('Houda.Chouket'));
insert into usermigration (oldusername, newusername) values ('indoye',lower('Ibrahima.Ndoye'));
insert into usermigration (oldusername, newusername) values ('jclevela',lower('James.Cleveland'));
insert into usermigration (oldusername, newusername) values ('jcossart',lower('James.Cossart'));
insert into usermigration (oldusername, newusername) values ('jccalvez',lower('JC.Calvez'));
insert into usermigration (oldusername, newusername) values ('jcbouver',lower('Jeanclement.Bouveres'));
insert into usermigration (oldusername, newusername) values ('jfcollin',lower('Jean-francois.Collin'));
insert into usermigration (oldusername, newusername) values ('jfmoenne',lower('Jean-Francois.Moenne'));
insert into usermigration (oldusername, newusername) values ('jlrauline',lower('Jean-Luc.Rauline'));
insert into usermigration (oldusername, newusername) values ('jmgiraul',lower('Jean-Marie.Girault'));
insert into usermigration (oldusername, newusername) values ('jvigneron',lower('Jeanmichel.Vigneron'));
insert into usermigration (oldusername, newusername) values ('jpdubuc',lower('Jean-Pierre.Dubuc'));
insert into usermigration (oldusername, newusername) values ('jlevy',lower('joelle.levy'));
insert into usermigration (oldusername, newusername) values ('jdossant',lower('Jose.Dos-Santos'));
insert into usermigration (oldusername, newusername) values ('jfournie',lower('Julien.Fournier'));
insert into usermigration (oldusername, newusername) values ('jmvillard',lower('jvillard'));
insert into usermigration (oldusername, newusername) values ('kmartine',lower('Kevin.Martineau'));
insert into usermigration (oldusername, newusername) values ('kmartineau',lower('Kevin.Martineau'));
insert into usermigration (oldusername, newusername) values ('lsigni',lower('Laetitia.Signi'));
insert into usermigration (oldusername, newusername) values ('lgervrau',lower('Laurent.Gervraud'));
insert into usermigration (oldusername, newusername) values ('lnolius',lower('Laurent.Nolius'));
insert into usermigration (oldusername, newusername) values ('lpelletier',lower('Lionel.Pelletier'));
insert into usermigration (oldusername, newusername) values ('mgrant',lower('marc.grant'));
insert into usermigration (oldusername, newusername) values ('mszerwin',lower('Marc.Szerwiniack'));
insert into usermigration (oldusername, newusername) values ('mcastanares',lower('Mariano.Castanares'));
insert into usermigration (oldusername, newusername) values ('mlemaire',lower('Marion.Lemaire'));
insert into usermigration (oldusername, newusername) values ('mcerez',lower('Michel.Cerez'));
insert into usermigration (oldusername, newusername) values ('mdelegli',lower('Mickael.Deleglise'));
insert into usermigration (oldusername, newusername) values ('nhinkle',lower('Natalie.Hinkle'));
insert into usermigration (oldusername, newusername) values ('nbaillette',lower('nicolas.baillette'));
insert into usermigration (oldusername, newusername) values ('npatou',lower('Nicolas.Patou'));
insert into usermigration (oldusername, newusername) values ('obegarie',lower('Olivier.Begarie'));
insert into usermigration (oldusername, newusername) values ('ogleniss',lower('Olivier.Glenisson'));
insert into usermigration (oldusername, newusername) values ('ogranger',lower('Olivier.Granger'));
insert into usermigration (oldusername, newusername) values ('oloones',lower('Olivier.Loones'));
insert into usermigration (oldusername, newusername) values ('oville',lower('Olivier.Ville'));
insert into usermigration (oldusername, newusername) values ('pfoulon',lower('Patrick.Foulon'));
insert into usermigration (oldusername, newusername) values ('plefebvr',lower('Philippe.Lefebvre'));
insert into usermigration (oldusername, newusername) values ('ppierre',lower('Philippe.Pierre'));
insert into usermigration (oldusername, newusername) values ('pinthavo',lower('Phone.Inthavong'));
insert into usermigration (oldusername, newusername) values ('pmillet',lower('Pierre.Millet'));
insert into usermigration (oldusername, newusername) values ('pseban',lower('Pierre.Seban'));
insert into usermigration (oldusername, newusername) values ('rmichel',lower('Romain.Michel'));
insert into usermigration (oldusername, newusername) values ('rrodrigu',lower('Ruben.Rodrigues'));
insert into usermigration (oldusername, newusername) values ('sslime',lower('Samir.Slime'));
insert into usermigration (oldusername, newusername) values ('sdubus',lower('Sandrine.Dubus'));
insert into usermigration (oldusername, newusername) values ('sniez',lower('Sandrine.Niez'));
insert into usermigration (oldusername, newusername) values ('ssablan',lower('Scott.Sablan'));
insert into usermigration (oldusername, newusername) values ('sbernard',lower('Sebastien.Bernard'));
insert into usermigration (oldusername, newusername) values ('scoquibu',lower('Stephane.Coquibus'));
insert into usermigration (oldusername, newusername) values ('sriche',lower('Stephane.Riche'));
insert into usermigration (oldusername, newusername) values ('tbonnet',lower('Thierry.Bonnet'));
insert into usermigration (oldusername, newusername) values ('tneusius',lower('Thierry.Neusius'));
insert into usermigration (oldusername, newusername) values ('twattecamps',lower('Thomas.Wattecamps'));
insert into usermigration (oldusername, newusername) values ('ttoulouse',lower('Tony.Toulouse'));
insert into usermigration (oldusername, newusername) values ('vcarrico',lower('vasco.carrico'));
insert into usermigration (oldusername, newusername) values ('vtran',lower('Victor.Tran'));
insert into usermigration (oldusername, newusername) values ('vdobler',lower('Vincent.Dobler'));
insert into usermigration (oldusername, newusername) values ('wlenormand',lower('william.le-normand'));
insert into usermigration (oldusername, newusername) values ('xverne',lower('xaverne'));
insert into usermigration (oldusername, newusername) values ('ythebault',lower('Yann.Thebault'));
insert into usermigration (oldusername, newusername) values ('ymekki',lower('Yassine.Mekki'));
insert into usermigration (oldusername, newusername) values ('yodemer',lower('Yoann.Odemer'));
insert into usermigration (oldusername, newusername) values ('yclorenn',lower('Yvon.Clorennec'));


SET SQL_SAFE_UPDATES=0; 

update jiraissue x inner join usermigration u on x.reporter = u.oldusername set x.reporter = u.newusername;

update jiraissue x inner join usermigration u on x.assignee = u.oldusername set x.assignee = u.newusername;
 
update jiraissue x inner join usermigration u on x.creator = u.oldusername set x.creator = u.newusername;

update jiraaction x inner join usermigration u on x.AUTHOR = u.oldusername set x.AUTHOR = u.newusername;

update jiraaction x inner join usermigration u on x.UPDATEAUTHOR = u.oldusername set x.UPDATEAUTHOR = u.newusername;

update changegroup x inner join usermigration u on x.AUTHOR = u.oldusername set x.AUTHOR = u.newusername;

update changeitem x inner join usermigration u on x.OLDVALUE = u.oldusername set x.OLDVALUE = u.newusername where x.field='assignee';

update changeitem x inner join usermigration u on x.NEWVALUE = u.oldusername set x.NEWVALUE = u.newusername where x.field='assignee';

update changeitem x inner join usermigration u on x.NEWVALUE = u.oldusername set x.NEWVALUE = u.newusername where x.field='reporter';

update changeitem x inner join usermigration u on x.OLDVALUE = u.oldusername set x.OLDVALUE = u.newusername where x.field='reporter';

update searchrequest x inner join usermigration u on x.authorname = u.oldusername set x.authorname = u.newusername; 

update searchrequest x inner join usermigration u on x.username = u.oldusername set x.username = u.newusername;

update schemepermissions x inner join usermigration u on x.perm_parameter = u.oldusername set x.perm_parameter = u.newusername where x.perm_type='user';

update membershipbase x inner join usermigration u on x.USER_NAME = u.oldusername set x.USER_NAME = u.newusername; 

update OS_CURRENTSTEP x inner join usermigration u on x.owner = u.oldusername set x.owner = u.newusername;

update OS_CURRENTSTEP x inner join usermigration u on x.caller = u.oldusername set x.caller = u.newusername;

update OS_HISTORYSTEP x inner join usermigration u on x.owner = u.oldusername set x.owner = u.newusername;

update OS_HISTORYSTEP x inner join usermigration u on x.caller = u.oldusername set x.caller = u.newusername; 

update fileattachment x inner join usermigration u on x.author = u.oldusername set x.author = u.newusername;

update filtersubscription x inner join usermigration u on x.username = u.oldusername set x.username = u.newusername;

update project x inner join usermigration u on x.lead = u.oldusername set x.lead = u.newusername; 

update userbase x inner join usermigration u on x.username = u.oldusername set x.username = u.newusername;

update customfieldvalue x inner join usermigration u on x.stringvalue = u.oldusername set x.stringvalue = u.newusername;

update columnlayout x inner join usermigration u on x.username = u.oldusername set x.username = u.newusername;

update portalpage x inner join usermigration u on x.username = u.oldusername set x.username = u.newusername;

update component x inner join usermigration u on x.LEAD = u.oldusername set x.LEAD = u.newusername;

update jiraworkflows x inner join usermigration u on x.creatorname = u.oldusername set x.creatorname = u.newusername;

update userassociation x inner join usermigration u on x.SOURCE_NAME = u.oldusername set x.SOURCE_NAME = u.newusername;

update cwd_membership x inner join usermigration u on x.child_name = u.oldusername set x.child_name = u.newusername;

update cwd_membership x inner join usermigration u on x.lower_child_name = u.oldusername set x.lower_child_name = LOWER(u.newusername);

update cwd_user x inner join usermigration u on x.user_name = u.oldusername set x.user_name = u.newusername,active=0;

update cwd_user x inner join usermigration u on x.lower_user_name = u.oldusername set x.lower_user_name = lower(u.newusername),active=0 where directory_id!=10100;

update external_entities x inner join usermigration u on x.NAME = u.oldusername set x.NAME = u.newusername;

Drop table tempo;

Create table tempo as select x.id as id from favouriteassociations x  inner join usermigration u on (lower(x.USERNAME)= lower(u.oldusername)) inner join favouriteassociations b on (lower(u.newusername) = lower(b.username) and x.entitytype=b.entitytype and x.entityid=b.entityid);

DELETE FROM favouriteassociations WHERE id in ( select id from tempo );

update favouriteassociations x inner join usermigration u on x.USERNAME = u.oldusername set x.USERNAME = u.newusername; 

Drop table tempo;

Create table tempo as select x.id as id from userhistoryitem x inner join usermigration u on (lower(x.USERNAME)= lower(u.oldusername)) inner join userhistoryitem b on (lower(u.newusername) = lower(b.username) and x.entitytype=b.entitytype and x.entityid=b.entityid);

DELETE FROM userhistoryitem WHERE id in (select id from tempo);

update userhistoryitem x inner join usermigration u on x.USERNAME = u.oldusername set x.USERNAME = u.newusername;

Drop table tempo;

Create table tempo as select x.id as id from userhistoryitem x  inner join usermigration u on (lower(x.entityid)= lower(u.oldusername)) inner join userhistoryitem b on (lower(u.newusername) = lower(b.entityid) and x.entitytype=b.entitytype and x.username=b.username);

DELETE FROM userhistoryitem WHERE id in (select id from tempo);

update userhistoryitem x inner join usermigration u on x.entityid = u.oldusername set x.entityid = u.newusername where entitytype = 'Assignee';

Drop table tempo;

update worklog x inner join usermigration u on x.AUTHOR = u.oldusername set x.AUTHOR = u.newusername;

update worklog x inner join usermigration u on x.UPDATEAUTHOR = u.oldusername set x.UPDATEAUTHOR = u.newusername;

update avatar x inner join usermigration u on x.owner = u.oldusername  set x.owner = u.newusername  where x.avatartype = "user";

update draftworkflowscheme x inner join usermigration u on x.last_modified_user = u.oldusername  set x.last_modified_user = u.newusername ;

create table tempo as select x.user_key as id from app_user x  inner join usermigration u on (x.user_key = lower(u.oldusername));

delete from app_user where user_key in (select id from tempo);

Drop table tempo;

drop table usermigration;