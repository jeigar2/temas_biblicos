lynx -dump -listonly https://www.vatican.va/archive/ESL0506/__P3.HTM
lynx -dump -dump_links 6 https://www.vatican.va/archive/ESL0506/__P3.HTM


lynx -dump -listonly https://www.vatican.va/archive/ESL0506/__P3.HTM | grep "6. "
   6. https://www.vatican.va/archive/ESL0506/__P4.HTM

#!/bin/bash

for i in {1..10}; do
  lynx -dump -listonly https://www.vatican.va/archive/ESL0506/__P3.HTM | grep -m 6 -o 'https.*\.HTM' | xargs lynx -dump -listonly
done