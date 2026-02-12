
-- Basic Dataset Health Check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT url) AS unique_urls,
    SUM(CASE WHEN extreme_low_price_flag = 1 THEN 1 ELSE 0 END) AS low_price_flag_count
FROM kijiji_rentals_clean;

-- Listings by Market Area
SELECT
    market_area,
    COUNT(*) AS listings,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_share
FROM kijiji_rentals_clean
GROUP BY market_area
ORDER BY listings DESC;

-- Average & Median Rent by Market Area
SELECT
  market_area,
  COUNT(*) AS listings,
  ROUND(AVG(price_monthly), 0) AS avg_price,
  QUANTILE_CONT(price_monthly, 0.25) AS p25_price,
  QUANTILE_CONT(price_monthly, 0.50) AS median_price,
  QUANTILE_CONT(price_monthly, 0.75) AS p75_price,
  MIN(price_monthly) AS min_price,
  MAX(price_monthly) AS max_price
FROM kijiji_rentals_clean
WHERE price_monthly IS NOT NULL
  AND extreme_low_price_flag = 0
GROUP BY market_area
HAVING COUNT(*) >= 30
ORDER BY median_price DESC;

-- Rent by Bedrooms and Market Area
SELECT
  market_area,
  bedrooms,
  COUNT(*) AS listings,
  QUANTILE_CONT(price_monthly, 0.50) AS median_price
FROM kijiji_rentals_clean
WHERE price_monthly IS NOT NULL
  AND extreme_low_price_flag = 0
  AND bedrooms IS NOT NULL
GROUP BY market_area, bedrooms
HAVING COUNT(*) >= 20
ORDER BY market_area, bedrooms;

-- Rent by Unit Type
SELECT
    unit_type_clean,
    COUNT(*) AS listings,
    AVG(price_monthly) AS avg_price,
    MEDIAN(price_monthly) AS median_price,
    MIN(price_monthly) AS min_price,
    MAX(price_monthly) AS max_price
FROM kijiji_rentals_clean
WHERE price_monthly IS NOT NULL
  AND extreme_low_price_flag = 0
GROUP BY unit_type_clean
ORDER BY median_price DESC;

-- Price per Square Foot by Market Area
SELECT
    market_area,
    COUNT(*) AS listings,
    ROUND(AVG(price_monthly / sqft), 2) AS avg_price_per_sqft,
    MEDIAN(price_monthly / sqft) AS median_price_per_sqft
FROM kijiji_rentals_clean
WHERE price_monthly IS NOT NULL
  AND sqft IS NOT NULL
  AND sqft > 0
  AND extreme_low_price_flag = 0
GROUP BY market_area
ORDER BY median_price_per_sqft DESC;

-- Inventory Mix by Unit Type and Market Area
SELECT
    market_area,
    unit_type_clean,
    COUNT(*) AS listings,
    ROUND(100.0 * COUNT(*) 
          / SUM(COUNT(*)) OVER (PARTITION BY market_area), 2) AS pct_within_market
FROM kijiji_rentals_clean
WHERE unit_type_clean IS NOT NULL
GROUP BY market_area, unit_type_clean
ORDER BY market_area, listings DESC;

-- Bedroom Premium Curve
SELECT
    bedrooms,
    COUNT(*) AS listings,
    QUANTILE_CONT(price_monthly, 0.50) AS median_price
FROM kijiji_rentals_clean
WHERE price_monthly IS NOT NULL
  AND extreme_low_price_flag = 0
  AND bedrooms IS NOT NULL
GROUP BY bedrooms
ORDER BY bedrooms;