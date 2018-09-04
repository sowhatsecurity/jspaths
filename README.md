### JS Paths

This little script extracts URL's from JavaScript files by performing the following - 

* For a given Domain, retrieves all of the Javascript files from Wayback (application/javascript)
* Each file is parsed for Relative and Absolute paths 
* Results are printed to the console


#### How to use:

```
python jspaths.py -d <domain>
```

#### Example:

```
python jspaths.py -d www.hackerone.com
```

```
Running query: http://web.archive.org/cdx/search/cdx?url=www.hackerone.com/*&output=json&fl=original&collapse=urlkey&filter=!statuscode:404&filter=mimetype:application/javascript&limit=2000000


Query Complete. Parsing Reuslts...

----------------------------------------------------------------------------------
https://hackerone.com/assets/constants-113b09620540bac78a582cb60afbc37ef7f68050ab15b5229a6b53465646868e.js
----------------------------------------------------------------------------------

****REL****

/images/demo_avatars/louise.png
/images/demo_avatars/kiera.png
/images/demo_avatars/joshua.png
/images/demo_avatars/liol.png
/images/demo_avatars/quinn.png

****AB****

https://www.hackerone.com
https://github.com/MyTeam/fancy_project

...
```

#### Credits:

* Relative Path RegEx came from the following previous work: https://github.com/jobertabma/relative-url-extractor
