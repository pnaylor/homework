"""
Finds the second lowest cost silver plan for a set of zip codes
Uses three csv input files in the same folder as this source
"""

# Input files
ZIPS_FILE = 'slcsp.csv'
RATE_AREAS_FILE = 'zips.csv'
RATES_FILE = 'plans.csv'

# Output file
RESULT_FILE = 'slcsp_results.csv'

#Column numbers
ZIP_COL = 0
STATE_COL = 1
METAL_COL = 2
RATE_COL = 3
AREA_COL = 4

SILVER_LEVEL = 'Silver'

def get_zip_codes():
    """ collect zip codes to search on from csv """
    zips = []
    with open(ZIPS_FILE, 'r') as file:
        for line in file:
            zips.append(line.strip(',\n'))
    del zips[0] # trim headers column
    return zips

def get_areas(zcode):
    """ find the rate areas for a given zip code """
    areas = set()
    with open(RATE_AREAS_FILE, 'r') as file:
        for line in file:
            line_parts = line.split(',')
            if line_parts[ZIP_COL] == zcode:
                areas.add(line_parts[STATE_COL] + line_parts[AREA_COL].strip())
    return areas

def get_rates(target_area):
    """ find all silver plan rates for a given rate area tuple """
    rates = set()
    with open(RATES_FILE, 'r') as file:
        for line in file:
            line_parts = line.split(',')
            metal_level = line_parts[METAL_COL]
            if metal_level != SILVER_LEVEL:
                continue # only need silver plans
            area = line_parts[STATE_COL] + line_parts[AREA_COL].strip()
            if area == target_area:
                rates.add(line_parts[RATE_COL])
    return rates

def main():
    """ generates output file """
    zip_codes = get_zip_codes()
    with open(RESULT_FILE, 'w') as results:
        results.write('zipcode,rate\n')
        for zcode in zip_codes:
            areas = get_areas(zcode)
            if len(areas) != 1:
                results.write(zcode + ',\n')
                continue # cannot isolate an answer for 0 or > 1 rate areas

            rates = get_rates(areas.pop())
            if len(rates) > 1:
                rates.discard(min(rates))
                results.write(zcode + ',' + min(rates) + '\n')
            else: # no slcsp found
                results.write(zcode + ',\n')

try:
    main()
except IOError:
    print("Can't find all input files!")
