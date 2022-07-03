# car-market-parser
This is a parser for car market. It uses data from [auto.ru](https://auto.ru/).

***You must set up config.json before running the script.***

***You may need to visit the site before running the script.***

### Config parameter values.
 - `log level`
   - `debug`, `info`, `warning`, `error`, `critical`

 - `url`
   - `region`
     - All regions on auto.ru.
   - `type_of_vehicle`
     - `cars`
     - `lcv` (light commercial vehicle), `trailer`, `crane`, `truck`, `agricultural`, `dredge`, `artic` (semi truck), `construction`, `bulldozers`, `bus`, `autoloader`, `municipal`
     - `motorcycle`, `scooters`, `atv`, `snowmobile`
     - `electro`
   - `vendor`
     - `vendor-foreign`, `vendor-domestic`
     - And all brands on auto.ru.
   - `model`
     - All models of selected brand on auto.ru.
   - `age`
     - `all`, `new`, `used`

 - `payload`
   - `search_tag`
     - `external_panoramas`, `certificate_manufacturer`, `wide-back-seats`, `big`, `handling`, `all-terrain`, `comfort`, `medium`, `oversize`, `sport`, `economical`, `fast`, `offroad`, `big-trunk`, `compact`, `new4new`, `style`, `prestige`, `liquid`, `options` (a wide range of options)
   - `color`
     - `040001`, `CACECB`, `FAFBFB`, `97948F`, `0000CC`, `EE1D19`, `007F00`, `200204`, `C49648`, `22A0F8`, `DEA522`, `660099`, `4A2197`, `FFD600`, `FF8649`, `FFC0CB`
   - `sort`
     - `relevance-asc`, `relevance-desc`
     - `cr_date-desc`, `cr_date-asc`
     - `price-acs`, `price-desc`
     - `year-desc`, `year-acs`
     - `km_age-asc`, `km_age-desc`
     - `alphabet-acs`, `alphabet-desc`

   - `exchange_group`
     - `possible`
   - `seller_group`
     - `commercial`, `private`
   - `owners_counter_group` (how many owners the car had)
     - `one`, `less_than_two`

   - `steering_wheel`
     - `left`, `right`
   - `transmission`
     - `mechanical`, `automatic`, `robot`, `variator`

   - `price_from`
   - `price_to`
   - `year_from`
   - `year_to`
   - `km_age_from`
   - `km_age_to`
   - `displacement_from`
   - `displacement_to`
   - `power_from`
   - `power_to`
   - `acceleration_from`
   - `acceleration_to`
   - `fuel_rate_to`
   - `clearance_from`
     - All parameters above contain an integer.

   - `pts_status`
     - `"1"` — original pts.
     - `"2"` — duplicate pts.

   - `with_warranty`
   - `online_view`
   - `has_image`
   - `has_video`
     - All parameters above contain boolean value.
 - `pages` — how many pages to parse.

### Output JSON.
 - `color`
   - Color in HEX.
 - `name`
   - Name of the vehicle.
 - `price`
   - Vehicle price.
 - `km_age`
   - Mileage in kilometers.
 - `year`
   - Year of issue.
 - `engine`
   - Engine info.
 - `place`
   - Place of sale.
