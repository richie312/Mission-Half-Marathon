-- SELECT max(Day) FROM RDS_MySql.mission_half_marathon;
-- select sum(DistanceCovered) from RDS_MySql.mission_half_marathon  where Day='2021-W32'

--  ALTER TABLE RDS_MySql.mission_half_marathon
--   ADD goal_distance int
--     AFTER Day;
-- select * from RDS_MySql.mission_half_marathon
-- select distinct(goal_distance) from RDS_MySql.mission_half_marathon  where Day='2021-W32'
delete from RDS_MySql.mission_half_marathon where goal_distance = 0