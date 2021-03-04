 use hikki;
 drop table if exists `tariff`;
 create table `tariff`(
     `id` INT UNIQUE AUTO_INCREMENT,
     `code` VARCHAR(40) not null ,
     `year` INT not null ,
     `value` double(30,10),
     primary key (`id`),
     foreign key (`code`) references `Code`(`code`),
    foreign key (`year`) references `Year`(`year`)
);


select tc.reporter as code1,C1.country as country1,C1.region as region1,
       tc.partner as code2,C2.country as country2,C2.region as region2,
       Y.year as year,
       pG1.value as GDP1,pG2.value as GDP2,
       (pcgdp1.value*GW1.value/100) as INV1,
       (pcgdp2.value*GW2.value/100) as INV2,
#        iw1.value as INV1,iw2.value as INV2,
       tc.value as tij,
       t1.value as tariff1,
       t2.value as tariff2 from tc
inner join Code C1 on tc.reporter = C1.code
inner join Code C2 on tc.partner = C2.code
inner join GDP_WDI GW1 on C1.code = GW1.code
inner join GDP_WDI GW2 on C2.code = GW2.code
inner join per_GDP pG1 on C1.code = pG1.code
inner join per_GDP pG2 on C2.code = pG2.code
# inner join inv_oecd iw1 on C1.code = iw1.code
# inner join inv_oecd iw2 on C2.code = iw2.code
inner join oecd_pcgdp pcgdp1 on C1.code = pcgdp1.code
inner join oecd_pcgdp pcgdp2 on C2.code = pcgdp2.code
inner join tariffVivid t1 on C1.code = t1.code
inner join tariffVivid t2 on C2.code = t2.code
inner join Year Y on (tc.year = Y.year
                          and t1.year = Y.year and t2.year=Y.year
                          and GW1.year = Y.year and GW2.year = Y.year
                          and pcgdp1.year = Y.year and pcgdp2.year = Y.year
#                         and iw1.year = Y.year and iw2.year=Y.year
                          and pG1.year = Y.year and pG2.year=Y.year
    )
where (tc.value is not null)
    and (GW1.value is not null) and (GW2.value is not null)
    and (pcgdp1.value is not null) and (pcgdp2.value is not null)
#   and (iw1.value is not null ) and (iw2.value is not null )
    and (t1.value is not null) and (t2.value is not null)
    and (pG2.value is not null ) and (pG1.value is not null )
    and (Y.year>=2000) and (Y.year<=2018)
    and (C1.region is not null) and (C2.region is not null)
;