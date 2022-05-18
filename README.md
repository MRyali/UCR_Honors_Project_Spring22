# UCR Honors CapStone Project: Food Index Score

# Project Information
* Completed Spring 2022
* Department of Computer Science and Enginnering at UCR
* Author:
  * Mayur Ryali
* Faculty Mentor
  * Dr. Paea LePendu
* Collaborators
  * Tyler Pastor      
  
<h1>Abstract</h1>

<d1>
    <dd> Food quality and availability may be a key social determinant of one’s medical health.
Giving a person the ability to see the quality and availability of food in the nearby area may lead
to an increase in healthier decisions and better medical AI. I worked with the Food Index Team
at UCR’s PiLabs to create an application using Python, pre-existing data-scraping and
data-tagging tools created by PiLabs, and the Google Places API. The application takes the
user’s current location or allows them to input a custom location. Upon inputting the location,
the application will provide the location of every food source (restaurant, market, etc) within a
five-mile radius. Each food source is then assigned a “food index score” that will be averaged to
assign the general area a score. This score will be derived from an algorithm that will consider
factors like the price, distance, and food nutritional facts for each food source. We used the
Ofcom United Kingdom Nutritional profiling model to evaluate the nutritional health of each
food source. The food index score will be on a scale from 1 to 5 with 5 being the best absolute
option and 1 being the worst. This app is a step toward identifying food swamps. This is
important because finding food swamps helps implement public policy to reduce the presence of
food-related diseases such as diabetes. </dd>    
</d1>

<br>

<h2>Running the Program</h2>

<d2>
* Clone and run python3 MapMain.py

  * Will require individual Google Places API key
</d2>
