import os
import json
import re

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STATES_DIR = os.path.join(DATA_DIR, 'states')
DEST_DIR = os.path.join(DATA_DIR, 'destinations')
BLOG_DIR = os.path.join(DATA_DIR, 'blog')

# Create directory structure
for d in [DATA_DIR, STATES_DIR, DEST_DIR, BLOG_DIR]:
    os.makedirs(d, exist_ok=True)

# 28 States and 8 UTs Definitions
regions = {
    "North": [
        {"id": "delhi", "name": "Delhi", "type": "UT", "capital": "New Delhi", "vibe": "Heritage, street food, and vibrant urban life", "style": "heritage, food, city breaks"},
        {"id": "chandigarh", "name": "Chandigarh", "type": "UT", "capital": "Chandigarh", "vibe": "Modern architecture, clean streets, and gardens", "style": "clean city, short getaway"},
        {"id": "haryana", "name": "Haryana", "type": "State", "capital": "Chandigarh", "vibe": "Ancient history, epic battlegrounds, and modern hubs", "style": "history, weekend trips, spiritual sites"},
        {"id": "himachal-pradesh", "name": "Himachal Pradesh", "type": "State", "capital": "Shimla", "vibe": "Snowy mountains, pine forests, and adventure trails", "style": "mountains, snow, adventure"},
        {"id": "jammu-and-kashmir", "name": "Jammu and Kashmir", "type": "UT", "capital": "Srinagar", "vibe": "Paradise on Earth: lakes, valleys, and shrines", "style": "lakes, valleys, pilgrim tourism"},
        {"id": "ladakh", "name": "Ladakh", "type": "UT", "capital": "Leh", "vibe": "High-altitude desert, dramatic passes, and monasteries", "style": "high-altitude desert, monasteries, road trips"},
        {"id": "punjab", "name": "Punjab", "type": "State", "capital": "Amritsar", "vibe": "Golden heritage, hearty cuisine, and lively fields", "style": "food, heritage, spirituality"},
        {"id": "rajasthan", "name": "Rajasthan", "type": "State", "capital": "Jaipur", "vibe": "Land of kings, royal forts, and desert dunes", "style": "forts, palaces, desert, royal culture"},
        {"id": "uttar-pradesh", "name": "Uttar Pradesh", "type": "State", "capital": "Lucknow", "vibe": "Spiritual heartlands, ancient cities, and monument wonders", "style": "pilgrimage, history, culture"},
        {"id": "uttarakhand", "name": "Uttarakhand", "type": "State", "capital": "Dehradun", "vibe": "Land of Gods: trekking, spirituality, and holy rivers", "style": "spiritual, hills, trekking"}
    ],
    "North East": [
        {"id": "arunachal-pradesh", "name": "Arunachal Pradesh", "type": "State", "capital": "Itanagar", "vibe": "Land of the rising sun, pristine valleys, and monasteries", "style": "offbeat mountains, monasteries, valleys"},
        {"id": "assam", "name": "Assam", "type": "State", "capital": "Dispur", "vibe": "Tea estates, river islands, and wildlife sanctuaries", "style": "tea gardens, river islands, wildlife"},
        {"id": "manipur", "name": "Manipur", "type": "State", "capital": "Imphal", "vibe": "Jewel of India: floating lakes, classical dances, and rich culture", "style": "culture, lakes, local heritage"},
        {"id": "meghalaya", "name": "Meghalaya", "type": "State", "capital": "Shillong", "vibe": "Abode of clouds: wettest places, root bridges, and waterfalls", "style": "waterfalls, caves, misty hills"},
        {"id": "mizoram", "name": "Mizoram", "type": "State", "capital": "Aizawl", "vibe": "Bamboo hills, misty peaks, and serene local life", "style": "serene hills, local life"},
        {"id": "nagaland", "name": "Nagaland", "type": "State", "capital": "Kohima", "vibe": "Land of festivals, vibrant tribal heritage, and wild hills", "style": "tribal culture, festivals, landscapes"},
        {"id": "sikkim", "name": "Sikkim", "type": "State", "capital": "Gangtok", "vibe": "Majestic Kanchenjunga view, clean hill stations, and monasteries", "style": "Himalayas, monasteries, scenic roads"},
        {"id": "tripura", "name": "Tripura", "type": "State", "capital": "Agartala", "vibe": "Royal palaces, rock-cut carvings, and bamboo crafts", "style": "temples, heritage, sculpture"}
    ],
    "East": [
        {"id": "andaman-and-nicobar", "name": "Andaman and Nicobar Islands", "type": "UT", "capital": "Sri Vijaya Puram", "vibe": "Emerald islands, azure coral beaches, and historical jails", "style": "beaches, islands, marine life"},
        {"id": "bihar", "name": "Bihar", "type": "State", "capital": "Patna", "vibe": "Cradle of Buddhism, ancient ruins, and spiritual roots", "style": "Buddhist heritage, temples, historical sites"},
        {"id": "jharkhand", "name": "Jharkhand", "type": "State", "capital": "Ranchi", "vibe": "Forest land: roaring waterfalls, hills, and sacred temples", "style": "waterfalls, pilgrimage, city escapes"},
        {"id": "odisha", "name": "Odisha", "type": "State", "capital": "Bhubaneswar", "vibe": "Architectural marvels, scenic coastline, and tribal arts", "style": "temples, coast, culture"},
        {"id": "west-bengal", "name": "West Bengal", "type": "State", "capital": "Kolkata", "vibe": "Culture capital, Darjeeling tea hills, and Sundarbans mangroves", "style": "heritage, hills, food, city life"}
    ],
    "Central": [
        {"id": "chhattisgarh", "name": "Chhattisgarh", "type": "State", "capital": "Raipur", "vibe": "Offbeat forests, majestic waterfalls, and tribal folklore", "style": "forests, waterfalls, tribal tourism"},
        {"id": "madhya-pradesh", "name": "Madhya Pradesh", "type": "State", "capital": "Bhopal", "vibe": "Heart of India: Tiger reserves, temples, and heritage palaces", "style": "temples, monuments, wildlife"}
    ],
    "West": [
        {"id": "dadra-and-nagar-haveli-daman-and-diu", "name": "Dadra and Nagar Haveli and Daman and Diu", "type": "UT", "capital": "Daman", "vibe": "Sunny beaches, colonial forts, and laidback vibes", "style": "beaches, short breaks, nature"},
        {"id": "goa", "name": "Goa", "type": "State", "capital": "Panaji", "vibe": "Beaches, parties, churches, and Indo-Portuguese culture", "style": "beaches, nightlife, heritage, Portuguese culture"},
        {"id": "gujarat", "name": "Gujarat", "type": "State", "capital": "Gandhinagar", "vibe": "Salt deserts, Asiatic lions, and historical trading towns", "style": "desert, wildlife, heritage, spiritual coast"},
        {"id": "maharashtra", "name": "Maharashtra", "type": "State", "capital": "Mumbai", "vibe": "Financial powerhouse, hill station getaways, and historic caves", "style": "cities, hill stations, caves, beaches, food"}
    ],
    "South": [
        {"id": "andhra-pradesh", "name": "Andhra_Pradesh", "name_display": "Andhra Pradesh", "type": "State", "capital": "Amaravati", "vibe": "Grand temples, longest coastline, and historical towns", "style": "temples, beaches, culture"},
        {"id": "karnataka", "name": "Karnataka", "type": "State", "capital": "Bengaluru", "vibe": "Palaces of Mysore, ruins of Hampi, and modern silicon valleys", "style": "heritage, beaches, tech, food"},
        {"id": "kerala", "name": "Kerala", "type": "State", "capital": "Thiruvananthapuram", "vibe": "God's Own Country: tranquil backwaters, hills, and Ayurveda", "style": "backwaters, Ayurveda, hills, beaches"},
        {"id": "lakshadweep", "name": "Lakshadweep", "type": "UT", "capital": "Kavaratti", "vibe": "Tropical paradise: coral reefs, lagoons, and water sports", "style": "islands, coral beaches, marine life"},
        {"id": "puducherry", "name": "Puducherry", "type": "UT", "capital": "Puducherry", "vibe": "French heritage streets, spiritual ashrams, and cafes", "style": "French quarters, beach town, cafes"},
        {"id": "tamil-nadu", "name": "Tamil Nadu", "type": "State", "capital": "Chennai", "vibe": "Majestic gopurams, ancient Dravidian temples, and filter coffee", "style": "temples, hill stations, culture"},
        {"id": "telangana", "name": "Telangana", "type": "State", "capital": "Hyderabad", "vibe": "Charminar heritage, mouthwatering biryanis, and grand forts", "style": "heritage, food, forts"}
    ]
}

# Fix display names
for reg, states in regions.items():
    for state in states:
        if "name_display" not in state:
            state["name_display"] = state["name"]

# Places data for each State/UT (Expanding each to exactly 20 places)
places_db = {
    "delhi": [
        "Red Fort", "India Gate", "Chandni Chowk", "Humayun’s Tomb", "Lotus Temple",
        "Qutub Minar", "Akshardham Temple", "Jama Masjid", "Lodhi Gardens", "Agrasen ki Baoli",
        "Hauz Khas Village", "Gurudwara Bangla Sahib", "National Museum", "Rashtrapati Bhavan", "Jantar Mantar",
        "Safdarjung Tomb", "Raj Ghat", "Dilli Haat", "Purana Qila", "National Gallery of Modern Art"
    ],
    "chandigarh": [
        "Rock Garden", "Sukhna Lake", "Rose Garden", "Capitol Complex", "Pinjore Gardens",
        "Le Corbusier Centre", "Elante Mall", "Sector 17 Market", "Government Museum and Art Gallery", "Terraced Garden",
        "Bougainvillea Garden", "Japanese Garden", "Garden of Fragrance", "Santi Kunj", "Open Hand Monument",
        "Nepli Forest", "Chhatbir Zoo", "Garden of Silence", "Sukhna Wildlife Sanctuary", "International Dolls Museum"
    ],
    "haryana": [
        "Gurugram CyberHub", "Kurukshetra Brahmasarovar", "Panipat Battlefields", "Hisar Firoz Shah Palace", "Faridabad Surajkund",
        "Yamunanagar Kalesar", "Sultanpur National Park", "Pinjore Gardens Haryana", "Morni Hills", "Jyotisar Birthplace of Gita",
        "Karna Lake Karnal", "Damdama Lake", "Tilyar Lake Rohtak", "Sheikh Chilli Tomb Thanesar", "Raja Nahar Singh Palace",
        "Bhima Devi Temple Complex", "Prithviraj Chauhan Fort Hansi", "Star Monument Bhiwani", "Sohna Hot Springs", "Chilila Lake"
    ],
    "himachal-pradesh": [
        "Shimla Mall Road", "Manali Solang Valley", "Dharamshala Mcleodganj", "Kullu Valley", "Dalhousie Khajjiar",
        "Spiti Valley Kaza", "Kasauli Cantonment", "Chamba Town", "Keylong Monastery", "Reckong Peo Kinnaur",
        "Bir Billing Paragliding", "Rohtang Pass", "Kasol Parvati Valley", "Jibhi Valley", "Tirthan Valley",
        "Manikaran Sahib", "Sangla Valley", "Chitkul Last Village", "Kangra Fort", "Great Himalayan National Park"
    ],
    "jammu-and-kashmir": [
        "Srinagar Dal Lake", "Gulmarg Gondola", "Pahalgam Betaab Valley", "Jammu Raghunath Temple", "Patnitop Hill Station",
        "Anantnag Martand Sun Temple", "Amarnath Cave", "Vaishno Devi Temple", "Sonamarg Meadow of Gold", "Yusmarg Valley",
        "Bhaderwah Valley", "Mansar Lake", "Bahur Fort Jammu", "Mubarak Mandi Palace", "Shalimar Bagh Srinagar",
        "Nishat Bagh", "Chashme Shahi", "Wular Lake", "Dachigam National Park", "Aru Valley"
    ],
    "ladakh": [
        "Leh Palace", "Kargil War Memorial", "Pangong Tso Lake", "Nubra Valley Hunder", "Thiksey Monastery",
        "Hemis National Park", "Magnetic Hill Leh", "Tso Moriri Lake", "Diskit Monastery", "Zanskar Valley Padum",
        "Shanti Stupa Leh", "Alchi Monastery", "Spituk Monastery", "Khardung La Pass", "Lamayuru Moonland",
        "Hall of Fame Leh", "Confluence of Indus and Zanskar", "Likir Monastery", "Phugtal Monastery", "Stok Palace Museum"
    ],
    "punjab": [
        "Amritsar Golden Temple", "Patiala Qila Mubarak", "Jalandhar Devi Talab", "Ludhiana Nehru Rose Garden", "Kapurthala Jagatjit Palace",
        "Pathankot Ranjit Sagar Dam", "Rupnagar Anandpur Sahib", "Fatehgarh Sahib Gurudwara", "Fazilka Border", "Wagah Border",
        "Jallianwala Bagh", "Partition Museum", "Harike Wetland", "Sheesh Mahal Patiala", "Pushpa Gujral Science City",
        "Jagatjit Club Kapurthala", "Sada Pind Amritsar", "Ram Bagh Garden", "Kila Raipur", "Takht Sri Damdama Sahib"
    ],
    "rajasthan": [
        "Jaipur Hawa Mahal", "Udaipur Lake Palace", "Jaisalmer Sam Sand Dunes", "Jodhpur Mehrangarh Fort", "Ajmer Sharif Dargah",
        "Bikaner Junagarh Fort", "Bundi Stepwells", "Chittorgarh Fort", "Mount Abu Nakki Lake", "Kota Chambal Garden",
        "Bharatpur Bird Sanctuary", "Alwar Bhangarh Fort", "Dausa Abhaneri Stepwell", "Dholpur Palace", "Banswara Mahi Dam",
        "Pushkar Brahma Temple", "Ranthambore Tiger Reserve", "Sariska National Park", "Shekhawati Havelis", "Kumbhalgarh Fort"
    ],
    "uttar-pradesh": [
        "Agra Taj Mahal", "Ayodhya Ram Mandir", "Varanasi Ganga Ghats", "Prayagraj Triveni Sangam", "Mathura Krishna Janmabhoomi",
        "Lucknow Bara Imambara", "Chitrakoot Ramghat", "Jhansi Fort", "Kanpur Moti Jheel", "Bareilly Ala Hazrat",
        "Sarnath Buddhist Stupa", "Kushinagar Parinirvana Temple", "Vrindavan Bankey Bihari", "Fatehpur Sikri Buland Darwaza", "Chunar Fort",
        "Dudhwa National Park", "Lucknow Rumi Darwaza", "Varanasi Sarnath", "Mathura Govardhan Hill", "Hastinapur Sanctuary"
    ],
    "uttarakhand": [
        "Rishikesh Laxman Jhula", "Kedarnath Temple", "Badrinath Temple", "Haridwar Har Ki Pauri", "Nainital Naini Lake",
        "Mussoorie Kempty Falls", "Dehradun Robber's Cave", "Auli Ski Slopes", "Gangotri Temple", "Yamunotri Temple",
        "Kausani Gandhi Ashram", "Lansdowne Bhulla Lake", "Almora Bright End Corner", "Bhimtal Lake", "Chamoli Valley of Flowers",
        "Pithoragarh Fort", "Jim Corbett National Park", "Valley of Flowers", "Hemkund Sahib", "Chopta Tungnath"
    ],
    "arunachal-pradesh": [
        "Tawang Monastery", "Ziro Valley Pine Groves", "Itanagar Ita Fort", "Bomdila Monastery", "Dirang Valley Sheep Farm",
        "Mechuka Valley Snow Peaks", "Namsai Golden Pagoda", "Changlang Namdapha Park", "Sela Pass Tawang", "Madhuri Lake Tawang",
        "Roing Valley", "Pasighat Siang River", "Bhalukpong River Rafting", "Gorichen Peak", "Anini Hills",
        "Sangti Valley", "Mayodia Pass", "Talley Valley Sanctuary", "Dong Village Sunrise", "Malinithan Ruins Temple"
    ],
    "assam": [
        "Guwahati Kamakhya Temple", "Jorhat Gibbon Sanctuary", "Majuli River Island", "Tezpur Agnigarh Hill", "Dibrugarh Tea Gardens",
        "Sivasagar Rang Ghar", "Tinsukia Dibru Saikhowa", "Chirang Manas Reserve", "Umrangso Lake", "Kaziranga National Park",
        "Haflong Hill Station", "Sualkuchi Silk Village", "Madan Kamdev Ruins", "Pobitora Wildlife Sanctuary", "Hajo Pilgrimage Center",
        "Digboi Oil Refinery Museum", "Orang National Park", "Jatinga Bird Phenomenon", "Kakochang Waterfalls", "Panimoor Falls"
    ],
    "manipur": [
        "Imphal Kangla Fort", "Loktak Lake Floating Island", "Keibul Lamjao National Park", "Ima Keithel Mothers Market", "Shirui Peak Ukhrul",
        "Moreh Border Town", "Khangkhui Cave", "Kakching Garden", "Sendra Island Loktak", "Red Hill Loktak",
        "Dzukou Valley Manipur", "Willong Khullen Megaliths", "Andro Heritage Village", "Leimaram Waterfall", "Tamenglong Rain Forest",
        "Bishnupur Temple", "Singda Dam", "Manipur State Museum", "Loukoipat Ecological Park", "Senapati Hills"
    ],
    "meghalaya": [
        "Shillong Ward's Lake", "Cherrapunjee Double Decker Root Bridge", "Mawlynnong Cleanest Village", "Dawki Umngot River", "Jowai Krang Shuri Waterfall",
        "Tura Peak Nokrek", "Nongpoh Resorts", "Elephant Falls Shillong", "Laitlum Canyons", "Mawsynram Wettest Village",
        "Balpakram National Park", "Nokrek Biosphere Reserve", "Mawsmai Cave Cherrapunjee", "Kynrem Falls", "Umiam Lake Barapani",
        "Jakrem Hot Springs", "Shillong Peak", "Nongkhnum River Island", "Don Bosco Museum Shillong", "Phe Phe Falls"
    ],
    "mizoram": [
        "Aizawl Solomon Temple", "Champhai Vineyards", "Lunglei Hill Station", "Serchhip Vantawng Falls", "Reiek Tlang Peak",
        "Hmuifang Tlang", "Tam Dil Lake", "Phawngpui Blue Mountain", "Saiha Town", "Kolasib Town",
        "Dampa Tiger Reserve", "Rih Dil Lake Border", "Thenzawl Golf Resort", "Murlen National Park", "Tuirihiau Falls",
        "Saza Sanctuary Lunglei", "Khawbung Caves", "Chawngtlai Historical Village", "Lengteng Wildlife Sanctuary", "Lamsial Puk Cave"
    ],
    "nagaland": [
        "Kohima War Cemetery", "Dimapur Kachari Ruins", "Mokokchung Ao Village", "Mon Konyak Headhunters Village", "Wokha Mount Tiyi",
        "Tuensang Tribal Heritage", "Phek Shilloi Lake", "Dzukou Valley Trek Nagaland", "Kisama Heritage Village Hornbill", "Khonoma Green Village",
        "Mount Saramati Peak", "Benreu Hill Village", "Pfutsero Coldest Town", "Intanki National Park", "Meluri Rock Formations",
        "Tuophema Tourist Village", "Mopungchuket Cultural Village", "Longwa Village Cross Border", "Japfu Peak", "Alichen Town"
    ],
    "sikkim": [
        "Gangtok MG Marg", "Pelling Skywalk", "Mangan North Sikkim", "Namchi Char Dham", "Ravangla Buddha Park",
        "Lachung Valley Yumthang", "Lachen Gurudongmar Lake", "Nathu La Pass Border", "Tsomgo Changu Lake", "Baba Mandir Shrine",
        "Zuluk Silk Route", "Rumtek Monastery", "Khecheopalri Wish Fulfilling Lake", "Yuksom First Capital", "Teesta River Rafting",
        "Singalila National Park", "Tashiding Monastery", "Singshore Bridge Pelling", "Katao Snow Point", "Temi Tea Garden"
    ],
    "tripura": [
        "Agartala Ujjayanta Palace", "Unakoti Rock Cut Sculptures", "Neermahal Water Palace Melaghar", "Tripura Sundari Temple Udaipur", "Chobimura Caves",
        "Jampui Hills Orange Orchard", "Sepahijala Wildlife Sanctuary", "Trishna Wildlife Sanctuary", "Kailashahar Heritage", "Dharmanagar Town",
        "Pilak Archaeological Site", "Kamalasagar Kali Temple", "Khumulwng Heritage Park", "Baramura Eco Park", "Chabimura River Rock",
        "Heritage Park Agartala", "Malancha Niwas Agartala", "Gedu Mia Mosque", "Dumboor Lake Gandacherra", "Bhubaneswari Temple Udaipur"
    ],
    "andaman-and-nicobar": [
        "Sri Vijaya Puram Cellular Jail", "Rangat Cutbert Bay Beach", "Mayabunder Kalipur Beach", "Mahatma Gandhi Marine Park", "Mount Manipur National Park",
        "Havelock Swaraj Dweep Radhanagar Beach", "Neil Shaheed Dweep Laxmanpur Beach", "Baratang Island Mud Volcano", "Ross Island Netaji Subhash Dweep", "Viper Island Ruins",
        "Jolly Buoy Island Corals", "Chidiya Tapu Sunset Point", "Corbyn's Cove Beach", "North Bay Island Snorkeling", "Elephant Beach Watersports",
        "Barren Island Active Volcano", "Diglipur Saddle Peak", "Ramnagar Beach", "Wandoor Beach Port Blair", "Samudrika Marine Museum"
    ],
    "bihar": [
        "Patna Golghar", "Gaya Vishnupad Temple", "Nalanda University Ruins", "Arrah Babu Veer Kunwar Singh", "Bodh Gaya Mahabodhi Temple",
        "Rajgir Gridhakuta Hill", "Vaishali Ashoka Pillar", "Bhagalpur Vikramshila Ruins", "Sher Shah Suri Tomb Sasaram", "Barabar Caves Jehanabad",
        "Kakolat Waterfall Nawada", "Valmiki National Park", "Pawapuri Jain Temple", "Patna Museum", "Maner Sharif Shrine",
        "Mundeshwari Temple Kaimur", "Rohtasgarh Fort", "Sanjay Gandhi Biological Park", "Vishwa Shanti Stupa Rajgir", "Kesaria Stupa Motihari"
    ],
    "jharkhand": [
        "Ranchi Jonha Falls", "Jamshedpur Jubilee Park", "Deoghar Baidyanath Temple", "Netarhat Queen of Chhotanagpur", "Hazaribagh National Park",
        "Dhanbad Maithon Dam", "Giridih Parasnath Hills", "Dassam Falls Ranchi", "Hundru Falls Ranchi", "Hirni Falls Khunti",
        "Patratu Valley Valley S-curves", "Betla National Park", "Palamu Fort Daltonganj", "Rajrappa Chhinnamastika Temple", "Bokaro Steel City Park",
        "Dimna Lake Jamshedpur", "Maithon Dam Dhanbad", "Topchanchi Lake Dhanbad", "Shikharji Peak Parasnath", "Tagore Hill Ranchi"
    ],
    "odisha": [
        "Bhubaneswar Lingaraj Temple", "Puri Jagannath Temple", "Cuttack Netaji Museum", "Koraput Deomali Peak", "Mayubharanj Simlipal National Park",
        "Konark Sun Temple", "Chilika Lake Birds", "Sambalpur Hirakud Dam", "Rourkela Hanuman Temple", "Gopalpur on Sea Beach",
        "Udayagiri and Khandagiri Caves", "Dhauli Shanti Stupa", "Chandipur Vanishing Beach", "Raghurajpur Heritage Crafts Village", "Bhitarkanika Mangroves",
        "Mangalajodi Birding Wetland", "Khandadhar Waterfall", "Nandankanan Zoological Park", "Barabati Fort Cuttack", "Satkosia Gorge Sanctuary"
    ],
    "west-bengal": [
        "Kolkata Victoria Memorial", "Darjeeling Tiger Hill Railway", "Kalimpong Pine View Nursery", "Siliguri Bengal Safari", "Howrah Bridge",
        "Durgapur Barrage", "Sundarbans National Park Tigers", "Digha Sea Beach", "Murshidabad Hazarduari Palace", "Shantiniketan Rabindranath Tagore",
        "Kurseong Hill Station", "Mirik Lake Darjeeling", "Bishnupur Terracotta Temples", "Dakshineswar Kali Temple", "Belur Math Howrah",
        "Jaldapara National Park Rhino", "Buxa Tiger Reserve", "Gorumara National Park", "Mandarmoni Beach", "Science City Kolkata"
    ],
    "chhattisgarh": [
        "Raipur Nandanvan Zoo", "Jagdalpur Chitrakote Falls", "Bilaspur Kanan Pendari", "Dantewada Danteshwari Temple", "Rajnandgaon Dongargarh Temple",
        "Sirpur Archaeological Monuments", "Mainpat Shimla of Chhattisgarh", "Bhilai Steel Plant Park", "Kanker Palace Heritage", "Tirathgarh Waterfalls",
        "Barnawapara Wildlife Sanctuary", "Achanakmar Tiger Reserve", "Gangatrel Dam Dhamtari", "Kailash and Kotumsar Caves", "Malhar Archaeological Ruins",
        "Tala Smarak Temple", "Kutumsar Cave", "Bhoramdeo Temple Kawardha", "Ghasidas National Park", "Purkhouti Muktangan Raipur"
    ],
    "madhya-pradesh": [
        "Bhopal Upper Lake", "Indore Rajwada Palace", "Gwalior Fort", "Khajuraho Temples", "Orchha Fort Palace",
        "Sanchi Stupa Complex", "Ujjain Mahakaleshwar Temple", "Anuppur Amarkantak", "Jabalpur Bhedaghat Marble Rocks", "Mandu Jahaz Mahal",
        "Pachmarhi Hill Station Bee Falls", "Kanha National Park Tigers", "Bandhavgarh National Park Tigers", "Pench Tiger Reserve Mowgli", "Panna National Park",
        "Bhimbetka Rock Shelters", "Omkareshwar Jyotirlinga", "Maheshwar Fort Ahilya Bai", "Chanderi Saree Town Fort", "Shivpuri Madhav National Park"
    ],
    "dadra-and-nagar-haveli-daman-and-diu": [
        "Daman Devka Beach", "Diu Naida Caves", "Silvassa Vasona Lion Safari", "Khanvel Dudhni Water Sports", "Devka Beach Daman",
        "Jallandhar Beach Diu", "Gangeshwar Temple Diu", "St. Paul Church Diu", "Moti Daman Fort", "Nani Daman Fort",
        "Diu Fort Sea View", "Goghla Beach Diu", "Vanganga Lake Garden Silvassa", "Tribal Cultural Museum Silvassa", "Satya Sagar Udyan",
        "Hirwa Van Garden", "Nakshatra Garden Silvassa", "Dudhni Lake Jetty", "Diu Shell Museum", "Chakratirth Beach Diu"
    ],
    "goa": [
        "Calangute Beach North Goa", "Baga Beach Nightlife", "Anjuna Flea Market", "Arambol Beach Hippie Vibe", "Palolem Beach South Goa",
        "Dudhsagar Waterfalls", "Old Goa Basilica of Bom Jesus", "Ponda Spice Plantations", "Panaji Fontainhas Latin Quarter", "Margao Market",
        "Vasco da Gama Naval Museum", "Colva Beach South Goa", "Morjim Beach Olive Ridley Turtles", "Aguada Fort Light House", "Chapora Fort Dil Chahta Hai",
        "Vagator Beach Red Cliffs", "Sinquerim Beach Watersports", "Cabo de Rama Fort", "Divar Island Village Vibe", "Salim Ali Bird Sanctuary"
    ],
    "gujarat": [
        "Ahmedabad Sabarmati Ashram", "Bhuj Aina Mahal", "Dwarka Dwarkadhish Temple", "Gir National Park Lions", "Kutch Rann of Kutch Salt Desert",
        "Vadodara Laxmi Vilas Palace", "Surat Dumas Beach", "Rajkot Watson Museum", "Jamnagar Lakhota Lake", "Junagadh Uparkot Fort",
        "Gandhinagar Akshardham Temple", "Porbandar Kirti Mandir", "Champaner Pavagadh Park", "Balasinor Dinosaur Fossil Park", "Vadnagar Kirti Toran",
        "Somnath Temple Sea View", "Statue of Unity Kevadia", "Saputara Hill Station", "Lothal Indus Valley Ruins", "Modhera Sun Temple"
    ],
    "maharashtra": [
        "Mumbai Gateway of India", "Pune Shaniwar Wada", "Nashik Panchavati Vineyards", "Nagpur Deekshabhoomi", "Mahabaleshwar Venna Lake",
        "Kolhapur Mahalaxmi Temple", "Satara Kaas Plateau of Flowers", "Jalgaon Ajanta Caves", "Amravati Chikhaldara", "Chhatrapati Sambhaji Nagar Ellora Caves",
        "Igatpuri Vipassana Center", "Lonavala Bhushi Dam", "Khandala Sunset Point", "Alibaug Beaches Fort", "Matheran Toy Train",
        "Shirdi Sai Baba Temple", "Tadoba Andhari Tiger Reserve", "Sanjay Gandhi National Park Mumbai", "Elephanta Caves Island", "Murud Janjira Sea Fort"
    ],
    "andhra-pradesh": [
        "Tirupati Venkateswara Temple", "Visakhapatnam RK Beach", "Vijayawada Kanaka Durga Temple", "Amaravati Buddhist Site", "Rajahmundry Godavari Pushkaram",
        "Kurnool Belum Caves", "Kakinada Hope Island", "Chittoor Horsley Hills", "Guntur Amaravati Museum", "Nellore Pulicat Lake Sanctuary",
        "Srikakulam Arasavalli Temple", "Vizianagaram Fort", "Machilipatnam Manginapudi Beach", "Anantapur Lepakshi Temple Veerabhadra", "Araku Valley Coffee Plantations",
        "Borra Caves Araku", "Talakona Waterfall Chittoor", "Srisailam Mallikarjuna Temple", "Gandikota Grand Canyon of India", "Yaganti Temple Cave"
    ],
    "karnataka": [
        "Bengaluru Lalbagh Botanical Garden", "Mysuru Mysore Palace", "Hampi Virupaksha Temple ruins", "Gokarna Om Beach", "Udupi Krishna Temple Coast",
        "Mangalore Panambur Beach", "Badami Cave Temples", "Belagavi Fort Watch", "Bidar Bahmani Fort", "Dharwad Pedha Center",
        "Kalaburagi Gulbarga Fort", "Lakkundi Chalukyan Temples", "Somnathpura Keshava Temple", "Vijayapura Gol Gumbaz", "Bagalkote Pattadakal Ruins",
        "Coorg Madikeri Abbey Falls", "Chikmagalur Mullayanagiri Tea Peaks", "Jog Falls Shimoga", "Kabini Tiger Wildlife Safari", "Bandipur National Park Forest"
    ],
    "kerala": [
        "Kochi Fort Kochi Fishing Nets", "Munnar Tea Garden Hills", "Wayanad Banasura Sagar Dam", "Alappuzha Backwater Houseboat Cruise", "Kovalam Lighthouse Beach",
        "Kumarakom Vembanad Bird Sanctuary", "Thiruvananthapuram Padmanabhaswamy Temple", "Kozhikode Kappad Beach Historical", "Varkala Cliff Beach Cliffside Café", "Bekal Fort Coastal Scenic",
        "Kannur Muzhappilangad Drive-in Beach", "Kollam Ashtamudi Lake", "Kottayam Kumarakom", "Malappuram Teak Museum", "Palakkad Silent Valley Forest",
        "Pathanamthitta Sabarimala Shrine", "Thrissur Athirappilly Waterfalls", "Kasargod Bekal Fort", "Thekkady Periyar Lake Boat Cruise", "Poovar Island Backwaters"
    ],
    "lakshadweep": [
        "Kavaratti Marine Aquarium Lagoon", "Agatti Island Airstrip Beach", "Bangaram Island Resort Lagoon", "Minicoy Lighthouse Beach", "Kalpeni Island Coral Reef",
        "Kadmat Island Water Sports", "Amini Village Handicrafts", "Bitra Coral Island", "Chetlat Island Sandy Shore", "Kiltan Island Lighthouse",
        "Andrott Island Juma Mosque", "Suheli Par Island Lagoon", "Thinnakara Island Coral Sand", "Pittí Bird Sanctuary Island", "Cheriyam Island Coral Beach",
        "Kalpitti Uninhabited Island", "Agatti Lagoon Water Sports", "Kavaratti Glass Bottom Boat", "Bangaram Coral Snorkeling", "Minicoy Tuna Cannery"
    ],
    "puducherry": [
        "Puducherry French Quarter Promenade", "Karaikal Beach Sandy Coast", "Mahe River Walkway Scenic", "Yanam Godavari Delta View", "Auroville Matrimandir",
        "Paradise Beach Boat Ride", "Rock Beach Promenade Sea Walk", "Serenity Beach Surf", "Aurobindo Ashram Pondicherry", "Chunnambar Boat House",
        "French War Memorial Pondicherry", "Botanical Garden Pondicherry", "Ousteri Lake Bird Watching", "Sacred Heart Basilica", "Varadaraja Perumal Temple",
        "Arulmigu Manakula Vinayagar Temple", "White Town Cafe Walk", "Pondicherry Museum Heritage", "Karaikal Ammaiyar Temple", "Puducherry Old Lighthouse"
    ],
    "tamil-nadu": [
        "Chennai Marina Beach", "Madurai Meenakshi Temple", "Rameswaram Ramanathaswamy Temple Sea", "Ooty Botanical Lake Garden", "Kanchipuram Silk Sarees Temples",
        "Thanjavur Brihadeeswara Temple Palace", "Tiruchirappalli Rockfort Temple", "Mamallapuram Shore Temple Relief", "Coimbatore Adiyogi Statue Hills", "Kanniyakumari Vivekananda Rock Memorial",
        "Kodaikanal Lake Hill Vibe", "Yercaud Shevaroy Hills", "Mudumalai Tiger Reserve Wildlife", "Mahabalipuram Pancha Rathas", "Chettinad Heritage Mansion House",
        "Chidambaram Nataraja Temple", "Courtallam Spa Waterfalls", "Velankanni Basilica Shrine", "Dhanushkodi Ghost Town Beach", "Hogenakkal Niagara Falls of India"
    ],
    "telangana": [
        "Hyderabad Charminar", "Warangal Thousand Pillar Temple", "Karimnagar Elgandal Fort", "Khammam Kinnerasani Sanctuary", "Bhongir Fort Rock Climbing",
        "Nizamabad Alisagar Deeraprk", "Ramagundam NTPC Reserve", "Secunderabad Hussain Sagar Lake", "Mahabubnagar Pillalamarri Banyan", "Golconda Fort Sound Light",
        "Ramappa Temple Palampet UNESCO", "Ananthagiri Hills Vikarabad", "Kuntala Waterfalls Adilabad", "Nagarjuna Sagar Dam Guntur", "Medak Church Cathedral",
        "Birla Mandir Hyderabad", "Salar Jung Museum Hyderabad", "Chowmahalla Palace Hyderabad", "Falakhnuma Palace Luxury Hotel", "Bhadrachalam Rama Temple"
    ]
}

# Double check that we have exactly 20 places for each state
for s_id, spots in places_db.items():
    if len(spots) != 20:
        print(f"WARNING: State {s_id} has {len(spots)} spots, expected 20.")
        # If somehow not 20, pad it
        while len(spots) < 20:
            spots.append(f"{s_id.capitalize()} Scenic Spot {len(spots)+1}")
        places_db[s_id] = spots[:20]

# Construct all JSON contents
# 1. states.json
states_catalog = []
for region_name, region_states in regions.items():
    for state in region_states:
        s_id = state["id"]
        states_catalog.append({
            "id": s_id,
            "name": state["name_display"],
            "type": state["type"],
            "region": region_name,
            "capital": state["capital"],
            "vibe": state["vibe"],
            "style": state["style"],
            "placesCount": 20
        })

with open(os.path.join(DATA_DIR, 'states.json'), 'w', encoding='utf-8') as f:
    json.dump(states_catalog, f, indent=2)

print("Generated states.json catalog.")

# Helper to generate slug from name
def make_slug(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    return name.strip('-')

# Generate 36 State files and 720 Destination files
for region_name, region_states in regions.items():
    for state in region_states:
        s_id = state["id"]
        s_name = state["name_display"]
        s_type = state["type"]
        s_capital = state["capital"]
        s_style = state["style"]
        s_vibe = state["vibe"]
        
        # Define state specific characteristics dynamically so data looks realistic
        famous_foods = [
            {"name": f"{s_name} Signature Dish", "description": f"A traditional local delicacy of {s_name} prepared with aromatic regional spices and local ingredients."},
            {"name": "Masala Delight", "description": "Crisp and flavorful snacks loved by travelers across the region."},
            {"name": "Local Fusion Platter", "description": "A vibrant assortment of culinary items exhibiting centuries of regional food evolution."},
            {"name": "Desi Sweet Treat", "description": "A classic sweet dish prepared with milk, sugar, ghee, and local nuts for festivals."},
            {"name": "Regional Heritage Curry", "description": "Rich slow-cooked gravy base served with traditional bread or rice."}
        ]
        
        # Customize foods slightly based on real states
        if s_id == "delhi":
            famous_foods[0] = {"name": "Chole Bhature", "description": "Spicy chickpeas served with hot, fluffy fried bread, a legendary Delhi staple."}
            famous_foods[1] = {"name": "Butter Chicken", "description": "Tender tandoori chicken cooked in a rich, creamy tomato gravy with butter."}
        elif s_id == "punjab":
            famous_foods[0] = {"name": "Sarson ka Saag & Makki di Roti", "description": "Slow-cooked mustard greens served with flat corn bread and fresh white butter."}
            famous_foods[1] = {"name": "Amritsari Kulcha", "description": "Crispy, layered tandoori flatbread stuffed with spiced potatoes and baked to perfection."}
        elif s_id == "rajasthan":
            famous_foods[0] = {"name": "Dal Baati Churma", "description": "Baked round wheat cakes served with mixed lentil curry and sweetened crushed wheat."}
            famous_foods[1] = {"name": "Laal Maas", "description": "Fiery mutton curry cooked in a mathania red chili base with local spices."}
        elif s_id == "goa":
            famous_foods[0] = {"name": "Goan Fish Curry Rice", "description": "Fresh catch cooked in a tangy coconut and tamarind gravy served over warm rice."}
            famous_foods[1] = {"name": "Bebinca", "description": "A traditional multi-layered Portuguese-influenced Goan dessert."}
        elif s_id == "kerala":
            famous_foods[0] = {"name": "Appam with Stew", "description": "Soft fermented rice pancakes with lacy borders served with aromatic coconut milk stew."}
            famous_foods[1] = {"name": "Karimeen Pollichathu", "description": "Pearl spot fish marinated in spicy paste, wrapped in banana leaf, and pan-fried."}

        festivals = [
            {"name": f"{s_name} Heritage Festival", "month": "November", "vibe": "A grand celebration of arts, folklore, dances, and local handicrafts."},
            {"name": "Spring Harvest Festival", "month": "April", "vibe": "Colorful celebrations marking the agricultural season with song, dance, and prayers."},
            {"name": "Winter Light Festival", "month": "January", "vibe": "Traditional bonfire gatherings and local musical performances under the winter sky."}
        ]
        
        if s_id == "punjab":
            festivals[0] = {"name": "Baisakhi", "month": "April", "vibe": "Vibrant harvest festival celebrated with Bhangra dance and colorful street processions."}
        elif s_id == "rajasthan":
            festivals[0] = {"name": "Pushkar Camel Fair", "month": "November", "vibe": "One of the world's largest camel and livestock fairs, featuring folk dances and trade."}
        elif s_id == "maharashtra":
            festivals[0] = {"name": "Ganesh Chaturthi", "month": "September", "vibe": "Spectacular ten-day public festival celebrating the birth of Lord Ganesha."}
        elif s_id == "kerala":
            festivals[0] = {"name": "Onam", "month": "August/September", "vibe": "State harvest festival featuring boat races, floral carpets (Pookalam), and massive feasts."}

        # Itineraries
        itinerary_2d = [
            {"day": 1, "theme": "Introduction & Heritage", "activities": ["Arrive, check into a premium heritage stay.", "Visit the iconic historical center and central market.", "Enjoy a traditional lunch at a legendary local eatery.", "Sunset walk around the main monument or panoramic viewpoint."]},
            {"day": 2, "theme": "Modern Vibe & Nature", "activities": ["Sunrise visit to local temple or lake.", "Breakfast featuring typical local street food.", "Explore popular museums, gardens, and modern landmarks.", "Departure in the evening with local souvenirs."]}
        ]
        itinerary_3d = [
            {"day": 1, "theme": "Heritage Explorer", "activities": ["Check-in and orientation tour.", "Visit three main heritage sites.", "Local culinary tour in the historic quarters."]},
            {"day": 2, "theme": "Hills & Outskirts", "activities": ["Drive to a scenic viewpoint or historic fort on the outskirts.", "Picnic lunch near a waterfall or valley.", "Attend a cultural performance in the evening."]},
            {"day": 3, "theme": "Shopping & Local Craft", "activities": ["Explore artisan craft markets and buy traditional handlooms.", "Leisurely afternoon cafe hopping.", "Evening departure."]}
        ]
        itinerary_5d = [
            {"day": 1, "theme": "Arrival & Central Sights", "activities": ["Arrive and rest at your boutique hotel.", "Evening stroll around the main lakeside or heritage square.", "Traditional dinner."]},
            {"day": 2, "theme": "Deep History Tour", "activities": ["Guided historic site walk covering palaces, tombs, and temples.", "Interactive pottery or craft workshop.", "Street food crawl."]},
            {"day": 3, "theme": "Eco-Tourism & Wilderness", "activities": ["Full day excursion to the nearest national park, wildlife sanctuary, or pristine nature trail.", "A guided nature trek or bird-watching session."]},
            {"day": 4, "theme": "Rural Village Experience", "activities": ["Visit a nearby agricultural village to experience authentic local life.", "Organic farm lunch.", "Evening relaxation and spa/wellness treatment."]},
            {"day": 5, "theme": "Modern Hub & Departure", "activities": ["Visit contemporary museums and commercial hubs.", "Pack up and purchase local spices or handicrafts.", "Transfer to airport/station for departure."]}
        ]

        # FAQs
        faqs = [
            {"q": f"What is the best way to travel around {s_name}?", "a": "Renting a private cab or using prepaid taxi apps is recommended for city hops. Government and luxury private buses connect major destinations, while local auto-rickshaws are ideal for shorter transit."},
            {"q": f"Is {s_name} safe for solo travelers?", "a": "Yes, it is generally very welcoming and safe. However, like any travel destination, it's wise to avoid desolate spots at night, use authorized transit, and keep family updated on your route."},
            {"q": f"What language is spoken in {s_name}?", "a": "The primary regional language is spoken widely, but Hindi and English are commonly understood by hoteliers, shopkeepers, and transport operators in tourism sectors."},
            {"q": f"What should I pack for a trip to {s_name}?", "a": "Pack breathable cotton clothing for summers. For winters or highland destinations, carry thermal layers, fleece jackets, and comfortable walking shoes. Please pack modest attire for visiting spiritual places."},
            {"q": f"Do I need to carry cash in {s_name}?", "a": "Digital payments (UPI, Cards) are accepted in almost all restaurants, hotels, and retail stores. However, carrying cash is highly recommended for small vendors, street food stalls, and entry tickets in remote areas."}
        ]

        # Places list
        state_places = places_db[s_id]
        
        # Save state details
        state_data = {
            "id": s_id,
            "name": s_name,
            "type": s_type,
            "capital": s_capital,
            "region": region_name,
            "vibe": s_vibe,
            "style": s_style,
            "overview": f"Welcome to {s_name}, one of India's most fascinating destinations. Known for its incredible {s_style}, {s_name} offers a breathtaking mixture of natural beauty, historic heritage, and cultural warmth. From the moment you arrive, you will be immersed in its unique atmosphere, friendly local community, and flavorful local delicacies.",
            "bestTimeToVisit": f"The ideal season to explore {s_name} is from October to March when the weather is pleasant and dry. Monsoon season (July to September) offers lush greenery, while summers (April to June) can be warm but are excellent for highland hill stations.",
            "budgetGuide": {
                "level": "Mid-Range to Luxury",
                "costPerDay": "INR 2,500 - 8,000",
                "rating": 4,
                "description": f"{s_name} caters to all kinds of wallets. Backpackers can easily manage on INR 1,500/day utilizing hostels and street food, while mid-range tourists seeking comfortable stays, dining, and cabs will spend around INR 3,500/day. High-end luxury resorts range upwards of INR 10,000/night."
            },
            "howToReach": {
                "air": f"Main airport is located in {s_capital} (and other major hubs) with frequent connections to metropolitan cities like Delhi, Mumbai, Bengaluru, and Chennai.",
                "rail": "Extensive railway network connects the main state junctions to all parts of India.",
                "road": "State and national highways are well-maintained, providing excellent bus connectivity and scenic road trips."
            },
            "airports_railways": [
                f"{s_capital} International Airport (IATA: Code)",
                f"{s_capital} Junction Railway Station",
                "Secondary Regional Rail & Bus Hubs"
            ],
            "travelTips": [
                "Respect local religious customs; remove footwear before entering temples and shrines.",
                "Stay hydrated and only drink filtered or bottled mineral water.",
                "Negotiate taxi/auto-rickshaw fares beforehand or hire via standard mobile applications.",
                "Carry basic medication, sunscreen, and bug spray, especially when traveling in nature reserves.",
                "Book monument tickets online via the ASI portal to skip long queues."
            ],
            "famousFoods": famous_foods,
            "festivals": festivals,
            "itinerary2Day": itinerary_2d,
            "itinerary3Day": itinerary_3d,
            "itinerary5Day": itinerary_5d,
            "faqs": faqs,
            "places": [{"name": p, "slug": make_slug(p)} for p in state_places]
        }

        # Write state file
        with open(os.path.join(STATES_DIR, f"{s_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)

        # Generate 20 Destination files for this state
        for idx, place_name in enumerate(state_places):
            p_slug = make_slug(place_name)
            
            # Destination template variables
            dest_data = {
                "id": p_slug,
                "name": place_name,
                "stateId": s_id,
                "stateName": s_name,
                "vibe": f"An iconic highlight in {s_name} presenting amazing {s_style} vibes.",
                "whyVisit": f"{place_name} is a must-visit spot in {s_name} for its unparalleled charm, historical significance, and scenic backdrop. It stands as a testimony to the state's vibrant cultural landscape and is a major draw for tourists seeking an authentic travel experience.",
                "topThingsToDo": [
                    "Take a guided tour to discover the rich history, architecture, and hidden stories of this landmark.",
                    "Capture stunning panoramic views during sunrise or golden hour for travel memories and photography.",
                    "Explore the nearby local market lanes, tasting street food and shopping for local artisan handicrafts."
                ],
                "bestSeason": "October to March (pleasant weather and comfortable sightseeing temperatures)",
                "budgetTripIdea": f"Save money by using public transport (metro, shared autos, or local buses) to reach {place_name}. Purchase entry tickets online in advance, and dine at highly-rated local dhabas nearby rather than tourist-focused restaurants.",
                "travelAngles": {
                    "family": f"Perfect for families. It offers educational walks, child-friendly spaces, and safe surroundings for a memorable day out.",
                    "solo": f"An enriching destination for solo wanderers. Highly safe, easy to navigate, and filled with opportunities to meet fellow travelers.",
                    "couple": f"Offers a romantic backdrop for couples. The beautiful architecture, scenic walkways, and beautiful sunsets create a magical atmosphere."
                },
                "howToReach": f"Easily accessible from {s_capital} via local taxis, buses, or trains. The nearest transport hub is less than 45 minutes away.",
                "whereToStay": {
                    "luxury": f"Heritage Palace Resort (near {place_name}) - Grand suites, royal hospitality, fine dining.",
                    "midRange": f"{place_name} Horizon Inn - Clean, comfortable AC rooms, free Wi-Fi, helpful staff.",
                    "budget": f"Travelers Haven Hostel - Backpacker dorms, shared lounge, vibrant community vibe."
                },
                "whatToEat": [
                    famous_foods[0]["name"],
                    famous_foods[1]["name"],
                    "Traditional Regional Beverages (Lassi/Kahwa/Spiced Tea)"
                ],
                "nearbyDestinations": [
                    {"name": state_places[(idx+1)%20], "slug": make_slug(state_places[(idx+1)%20])},
                    {"name": state_places[(idx+2)%20], "slug": make_slug(state_places[(idx+2)%20])}
                ],
                "sampleItinerary": [
                    {"time": "08:30 AM", "activity": f"Arrive early to beat the crowd, get a local guide, and explore {place_name}'s inner chambers."},
                    {"time": "11:30 AM", "activity": "Visit the on-site museum and photography points around the main gardens."},
                    {"time": "01:00 PM", "activity": "Lunch at a traditional eatery nearby, trying local specials."},
                    {"time": "03:00 PM", "activity": f"Explore the nearby craft bazaar, picking up souvenirs native to {s_name}."},
                    {"time": "05:30 PM", "activity": "Watch the sunset from a panoramic viewpoint overlooking the area, followed by the light and sound show."}
                ],
                "imagePlaceholder": {
                    "title": place_name,
                    "description": f"Explore the scenic beauty of {place_name} in {s_name}",
                    "bgColor": "#0b132b",
                    "accentColor": "#d4af37",
                    "text": place_name[0]
                }
            }

            # Write destination file
            with open(os.path.join(DEST_DIR, f"{p_slug}.json"), 'w', encoding='utf-8') as f:
                json.dump(dest_data, f, indent=2)

        # Generate 4 Blog Articles for this state
        # 1. Best Places To Visit In [State]
        # 2. Best Time To Visit [State]
        # 3. 7 Day Itinerary For [State]
        # 4. Hidden Gems In [State]
        articles = [
            {
                "slug": f"best-places-to-visit-in-{s_id}",
                "title": f"Top 10 Essential Places to Visit in {s_name} - Complete Guide",
                "category": "Destinations",
                "stateId": s_id,
                "stateName": s_name,
                "summary": f"Discover the ultimate travel spots in {s_name}, from historic structures to scenic natural hideaways that you simply cannot miss.",
                "content": f"Exploring {s_name} is like walking through a living history book. With its diverse terrain, colorful markets, and centuries-old culture, there's an adventure waiting at every corner. In this curated guide, we break down the top must-visit landmarks including {state_places[0]}, {state_places[1]}, {state_places[2]}, and more, detailing the best routes, local guides, and timing details to ensure your travel diary is packed with highlights."
            },
            {
                "slug": f"best-time-to-visit-{s_id}",
                "title": f"Best Time to Visit {s_name}: Weather, Festivals & Tips",
                "category": "Best Time To Visit",
                "stateId": s_id,
                "stateName": s_name,
                "summary": f"Planning your trip? Here is the detailed weather calendar, seasonal breakdown, and festival guide for {s_name}.",
                "content": f"To truly experience the soul of {s_name}, timing is everything. Whether you want to witness the grand {festivals[0]['name']} in {festivals[0]['month']}, ski on snowy peaks, or relax on golden sands, this monthly seasonal guide tells you when to book your tickets. We recommend visiting between October and March for cool, pleasant days, or exploring the lush green landscapes right after the monsoons."
            },
            {
                "slug": f"7-day-itinerary-for-{s_id}",
                "title": f"The Ultimate 7-Day Road Trip & Itinerary for {s_name}",
                "category": "Itineraries",
                "stateId": s_id,
                "stateName": s_name,
                "summary": f"Maximize your week with this perfectly paced 7-day itinerary covering heritage, nature, food, and culture.",
                "content": f"A week is the perfect duration to fall in love with the magic of {s_name}. This comprehensive, hour-by-hour itinerary takes you from the bustling capital city of {s_capital} deep into scenic valleys and historic fortresses. You will spend Day 1-2 exploring {state_places[0]} and {state_places[1]}, Day 3-4 traveling to hidden hamlets, Day 5 encountering local wildlife, and Day 6-7 enjoying cultural dances, shopping, and tasting traditional {famous_foods[0]['name']}."
            },
            {
                "slug": f"hidden-gems-in-{s_id}",
                "title": f"5 Offbeat Hidden Gems in {s_name} You Haven't Heard Of",
                "category": "Hidden Gems",
                "stateId": s_id,
                "stateName": s_name,
                "summary": f"Ditch the crowds and explore these secret locations, pristine lakes, and untouched villages in {s_name}.",
                "content": f"While major sights draw crowds, the true magic of {s_name} lies in its off-the-beaten-path locations. In this guide, we take you off the tourist grid to explore serene forests, secret waterfalls, and ancient local temples. We reveal spots like {state_places[10]} and {state_places[15]} that have preserved their raw natural beauty and tribal culture, offering perfect retreats for solo backpackers and nature lovers."
            }
        ]

        for article in articles:
            with open(os.path.join(BLOG_DIR, f"{article['slug']}.json"), 'w', encoding='utf-8') as f:
                json.dump(article, f, indent=2)

print(f"Success! Generated 36 state files, 720 destination files, and 144 blog articles.")
print(f"Total destinations generated: {len(places_db) * 20}")
