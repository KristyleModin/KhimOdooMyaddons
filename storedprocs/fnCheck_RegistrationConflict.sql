CREATE OR REPLACE FUNCTION fnCheck_RegistrationConflict(reg_id BIGINT)
RETURNS TABLE (
    rid INT,
    rmessage VARCHAR   
) AS $$
DECLARE tdfrom DATE;
DECLARE tdto DATE;
DECLARE cnt INT;
DECLARE msg VARCHAR;
DECLARE troom_id BIGINT;
BEGIN
    -- get room schedule of registration
	
	select room_id,
	    cast("datefromSched" as DATE),
		cast("datetoSched" as DATE)
	into troom_id,tdfrom,tdto	
	from hotel_guestregistration 
	-- no index is required here since id is the primary key and automatically indexed
	where id=reg_id;
	
	select room_id,count(*)
	into cnt
	from hotel_guestregistration 
	-- note: an index on room_id and state should be supplied to avoid performance problems
	where room_id=troom_id and 
	  state in ('RESERVED','CHECKEDIN')
	  and ("datefromSched"  between tdfrom and tdto
		   or "datetoSched"  between tdfrom and tdto
		   or tdfrom between "datefromSched" and "datetoSched"
		   or tdto  between "datefromSched" and "datetoSched")
	  and id<>reg_id
	group by room_id;  
	  
	
	IF cnt > 0 THEN
	   msg:='Schedule conflict exists!';
	ELSE
	   msg:= 'No schedule conflict found';
	END IF;
	
	RETURN QUERY
	-- return result with cnt converted to 0 if null 
	select COALESCE(cnt,0),msg;
END;
$$ LANGUAGE plpgsql;