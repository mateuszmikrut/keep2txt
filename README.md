# keep2txt

This is a small tool to convert exported files from Google Keep to the txt format.


## Scenario/Instruction

1. Go to https://takeout.google.com/ and export your data (select at least Keep) - it takes some time to get a link  
2. Unzip your exported data  
     unzip takeout-*.zip 
3. Covert notes  
     ./keep2txt.py -s ~/Downloads/Takeout/Keep/ -d ~/Nextcloud/Notes/

    

