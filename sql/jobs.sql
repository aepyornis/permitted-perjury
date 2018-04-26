SELECT
  r.ucbbl as bbl,
  dobjobs.job as job,
  FIRST(dobjobs.prefilingdate) as prefilingdate,
  MAX(dobjobs.approved) as date_approved,
  MAX(dobjobs.latestactiondate) as latest_action_date,
  FIRST(dobjobs.jobtype) as jobtype,
  FIRST(dobjobs.ownername) as ownername,
  FIRST(dobjobs.address) as address,
  STRING_AGG(dobjobs.jobdescription, '|') as jobdescription,
  MAX(dobjobs.existingoccupancy) as existing_occupancy,
  anyarray_uniq(array_agg(dobjobs.jobtype)) as all_jobtypes,
  MAX(dobjobs.latestactiondate) as latest_action_date,
  FIRST(r.uc2008) as unitcount2008,
  FIRST(r.uc2009) as unitcount2009,
  FIRST(r.uc2010) as unitcount2010,
  FIRST(r.uc2011) as unitcount2011,
  FIRST(r.uc2012) as unitcount2012,
  FIRST(r.uc2013) as unitcount2013,
  FIRST(r.uc2014) as unitcount2014,
  FIRST(r.uc2015) as unitcount2015,
  FIRST(r.uc2016) as unitcount2016,
  GREATEST(
    FIRST(r.uc2008),
    FIRST(r.uc2009),
    FIRST(r.uc2010),
    FIRST(r.uc2011),
    FIRST(r.uc2012),
    FIRST(r.uc2013),
    FIRST(r.uc2014),
    FIRST(r.uc2015),
    FIRST(r.uc2016)
  ) as highest_unit_count
FROM
  rentstab r
  LEFT JOIN dobjobs on dobjobs.bbl = r.ucbbl
WHERE
  dobjobs.id IS NOT NULL
  AND dobjobs.jobtype <> 'A3'
  AND dobjobs.prefilingdate >= '2016-01-01'
GROUP BY
  dobjobs.job,
  r.ucbbl
ORDER BY
  latest_action_date desc
