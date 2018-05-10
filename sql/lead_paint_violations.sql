SELECT distinct bbl
FROM hpd_violations
WHERE novdescription like '%LEAD-BASED PAINT HAZARD%'
      AND "class" = 'C'
      AND date_part('year', novissueddate) in (2015,2016,2017)
