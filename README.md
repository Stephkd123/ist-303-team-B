Olympic Transport Guide - Part A
Team Members- 
1.	Rhett Carter
2.	Stephen Keyen
3.	Rohini Vishwanathan
4.	Tracy Gaolese
5.	Charlize Andaya

GitHub Repository: https://github.com/Stephkd123/ist-303-team-B.git 

Project Description
The Olympic Transport Guide is an AI-driven transport recommendation application designed to assist visitors and attendees of the 2028 Los Angeles Olympic Games in navigating the city efficiently. The app will provide real-time traffic updates, public transit schedules, ride-sharing integrations (Uber, Lyft), and eco-friendly transport options.
The system will personalize recommendations based on user location, budget, sustainability preferences, and time constraints to ensure an optimal travel experience during the event.

Relevant Project Stakeholders
1.	End Users (Olympic Visitors & Tourists): Travelers needing real-time transport recommendations.
2.	Los Angeles Public Transit Authorities: Agencies managing buses, metro, and other public transport systems.
3.	Ride-sharing Companies (Uber, Lyft, etc.): Private transport service providers.
4.	City of Los Angeles Government: Regulatory bodies overseeing transport policies.
5.	Local Businesses & Hotels: Hotels and businesses benefiting from tourism.
6.	Olympic Organizing Committee: Officials planning logistics for the Games.
7.	Tech Development Team: Developers, UI/UX designers, and data engineers building the app.
8.	Marketing & Outreach Team: Teams responsible for promoting and educating users about the app.
9.	Accessibility Advocacy Groups: Organizations ensuring the app supports wheelchair-friendly routes and inclusive travel solutions.
10.	Data Providers: Google Maps API, LA Metro API, and real-time traffic monitoring systems.
11.	Sustainability Partners: Companies supporting electric scooters, bike-sharing, and EV ride-share options.

User Stories
1.	As a visitor, I want to enter my location and destination to receive transport recommendations so that I can choose the best option.
•	Estimated Time: 10 days
2.	As a visitor, I want to see estimated travel time and cost for each transport option so that I can plan my trip effectively.
•	Estimated Time: 7 days
- Research and gather APIs to estimate travel time and cost (e.g., Google Maps, Uber, Lyft, and public transit APIs).
- Design the UI layout to display travel time and cost for different transport options.
- Implement API integration to fetch travel time and cost
- Process and structure API data for seamless display in the app.
- Implement filtering/sorting functionality for different transport modes.
- Test API responses for accuracy and performance.
- Conduct user testing to ensure usability and effectiveness.
- Document implementation details and known issues.

4.	As a visitor, I want to receive real-time traffic and transit updates so that I can avoid delays.
•	Estimated Time: 12 days
5.	As a visitor, I want to see the nearest public transport stations or ride-sharing pickup points so that I can easily access transport options.
•	Estimated Time: 8 days (Charlize Andaya)
- Use GPS to find the user’s location.
- Get data on public transport stations (bus, metro, train) and ride-sharing pickup points (Uber, Lyft) from APIs.
- Show nearest locations on an interactive map. 
- Display transportation options in a list for accessibility. 
- Build a filter for users to choose between public transport, ride-sharing, or both.  
- Have a search feature so users can manually enter a location and find its nearby public transport stations/ride-sharing pickup points.
- Show details on wait times, prices, and distance for transport options. 
- Test location/transport options and fix bugs/issues. 
  
6.	As an event attendee, I want to filter transport options based on sustainability (e.g., public transport and e-scooters) so that I can choose eco-friendly options.
•	Estimated Time: 6 days
7.	As a ride-sharing user, I want to integrate my Uber/Lyft account so that I can book a ride directly from the app.
•	Estimated Time: 15 days
8.	As a visitor, I want to receive recommendations based on budget preferences so that I can choose an affordable transport option.
•	Estimated Time: 6 days (Stephen Keyen)
- tasks (3days) - Defining budget criteria (i.e low: <$5, medium: $5-$10, high: >$10)
- Modify API for budget filtering
- Write unit tests(using pytest)
- tasks2 (3days) - Enhance sorting logic
- Add Error handling
- Optimize API response format
- final testing and documentation
9.	As an admin, I want to manage transport service integrations to ensure accurate data updates.
•	Estimated Time: 10 days
10.	As a developer, I want to integrate an interactive map feature so that users can visualize transport routes.
•	Estimated Time: 14 days
11.	As a visitor, I want the app to provide emergency transport options (e.g., hospitals and police stations) so that I can quickly access help if needed.
•	Estimated Time: 8 days
12.	As a visitor, I want the app to offer multilingual support so that I can navigate it in my preferred language.
•	Estimated Time: 7 days
13.	As a visitor with disabilities, I want the app to highlight wheelchair-friendly transport options so that I can travel independently.
•	Estimated Time: 8 days
14.	As a visitor, I want AI to learn my preferences and suggest optimized routes so that I can travel more efficiently.
•	Estimated Time: 10 days

Meeting Notes

Meeting Date: 02/26
We briefly met to discuss our individual progress on decomposing our user stories into tasks. Each group member will be in charge of one user story and its tasks. The five user stories we will be focusing on are:
- As a visitor, I want to enter my location and destination to receive transport recommendations so that I can choose the best option.  Estimated Time: 10 days (Rhett)
- As a visitor, I want to see estimated travel time and cost for each transport option so that I can plan my trip effectively. Estimated Time: 7 days (Tracy)
- As a visitor, I want to see the nearest public transport stations or ride-sharing pickup points so that I can easily access transport options. Estimated Time: 8 days (Charlize)
- As an event attendee, I want to filter transport options based on sustainability (e.g., public transport and e-scooters) so that I can choose eco-friendly options. Estimated Time: 6 days (Rohini)
- As a visitor, I want to receive recommendations based on budget preferences so that I can choose an affordable transport option. Estimated Time: 6 days (Stephen)

We plan on writing individual documents of the tasks for our assigned user stories to make updating the README easier. Rhett will be updating the README to reflect the tasks we listed for each user story. We also discussed briefly that the burn down chart to monitor our team’s progress will be completed by today’s class session.  We will also be uploading meeting notes from today 02/26 and this past Sunday 02/23. 



