import re
R = (
  r'^'
  r'[A-Z]{1,2}'   # Postal area
  r'[0-9]{1,2}'   # Postal district
  r'[A-Z]?'       # Optional subdistrict (London PAs only)
  r' '
  r'[0-9][A-Z]'   # Incode. Always one digit plus two letters
  r'$'
)

print(re.compile(R))
