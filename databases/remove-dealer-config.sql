do $$
DECLARE dcvalue text;
BEGIN
  dcvalue := '519ORANGEVILLEHONDA';
--   dcvalue := :dealercode;
  delete from newdealers.dealer_config where dealer_code like ('%' || dcvalue || '%');
  delete from newdealers.dealer_product_parameter where dealer_product_id in (
      select id from newdealers.dealer_product where dealer_code like ('%' || dcvalue || '%'));
  delete from newdealers.dealer_product where dealer_code like ('%' || dcvalue || '%');
  delete from newdealers.dealer_solution where dealer_code like ('%' || dcvalue || '%');
END $$;
