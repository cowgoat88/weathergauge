#GET NOAA FORECAST AND RUN METRICS v1.0
import urllib2
import re
import time
	
def create_metrics(html):
	strength_meter  = re.findall('STRONG',html)
	incoming_meter = re.findall('INCOMING|INCREASING',html)
	rain_meter = re.findall('RAIN',html)
	heavy_meter = re.findall('HEAVY',html)
	light_meter = re.findall('LIGHT',html)
	decreasing_meter = re.findall('DECREASING',html)
	weak_meter = re.findall('WEAK',html)
	intensity_rating = (len(strength_meter)+len(incoming_meter)+len(rain_meter)+len(heavy_meter))-(len(light_meter)+len(decreasing_meter)+len(weak_meter))
	print 'INTENSITY RATING : ', intensity_rating
	return intensity_rating

def get_html():
	noaa_text = 'http://forecast.weather.gov/product.php?site=MTR&issuedby=MTR&product=AFD&format=TXT&version=%d&glossary=1' % i
	response = urllib2.urlopen(noaa_text)
	time.sleep(0.1)
	html = ''.join(response.read())
	html_text = re.search('</SCRIPT>.*CONTENT ENDS HERE', html, re.MULTILINE|re.DOTALL)
	html_date = re.search('(\d*)\s(AM|PM)\sPST\s(\w{3})\s(\w{3})\s(\d*)\s(\d{4})', html_text.group(0))
	timestamp = html_date.group(1)+html_date.group(2)+'_'+html_date.group(4)+html_date.group(5)+'_'+html_date.group(6)
	
	return html_text.group(0), timestamp
	
for i in xrange(1,50):
	
	html,timestamp = get_html()
	file_id = str(hash(html))
	with open('file_id_file.txt','a+') as f_id:
		f_id_list = f_id.readlines()
		f_id_list = [x.rstrip() for x in f_id_list]
		if file_id in f_id_list:
			print 'file %s already exists' % file_id
			break
		else:
			print 'file %s created - %s' % file_id, timestamp
			metric = create_metrics(html)
			f_id.write(file_id+'\n')
			file_name = 'noaa_html_metrics.txt
			file_data = metric+'\t'+time.strftime('%d%m%y-%H%M%S_')+'\n'
			with open(file_name, 'a+') as f_html:
				f_html.write(file_data)
				
			
	f_id.close()
	
	
	
#add more variables for metrics
#integrate date/time code into ratings - timestamp regex created
#write files to subfolder 'html'

