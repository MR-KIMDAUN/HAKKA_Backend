-- Query: insert user_info
insert into tb_user_info (
        user_uuid, 
        user_id, 
        user_name, 
        user_pw, 
        nick_name, 
        user_profile, 
        use_yn, 
        reg_dt,
        chg_dt
    ) value (
        %s, 
        %s, 
        %s,
        %s, 
        %s,
        %s,
        %s,
        now(),
        now()
    );

-- Query: insert mokkoji_info
insert into tb_mokkoji_info (
        mokkoji_uuid, 
        mokkoji_name, 
        mokkoji_des, 
        reg_id, 
        reg_dt, 
        chg_id, 
        chg_dt, 
        use_yn
    ) value (
        %s, 
        %s, 
        %s,
        %s, 
        now(), 
        %s, 
        now(), 
        %s
    );

-- Query: select mokkoji_info & mokkoji_user
select *
    from tb_mokkoji_info a
    left join tb_user_info b
    on a.reg_id = b.user_id;

-- Query: insert Place_info
insert into tb_place_info (
        place_uuid, 
        mokkoji_uuid,
        place_cd,
        place_name,
        place_addr,
        place_explain,
        place_profile, 
        use_yn,
        reg_id, 
        reg_dt, 
        chg_id, 
        chg_dt,
        place_url 
    ) value (
        %s, 
        %s, 
        %s,
        %s, 
        %s, 
        %s, 
        %s,
        %s, 
        %s, 
        now(), 
        %s,
        now(),
        %s 
    );
    
-- Query: select place_info
select
	mokkoji_uuid,
	place_name,
	place_addr,
	place_explain,
	place_profile,
	place_url,
	reg_id,
	reg_dt 
from hakka.tb_place_info
where mokkoji_uuid = '1'
order by reg_dt asc;
