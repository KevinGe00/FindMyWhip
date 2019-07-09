# FindMyWhip

This project was developed in a four person team including an experienced third year developer, a third year electrical engineer, a first year computer science student, and myself. 

The goal of this project was to help people who may be visiting an unfamiliar place or people with disabilities to find there car without having to remember to tag there location like leading competitors. People with a smart car would have to register there car online on the smart car interface. When they needed to find there car, they would simply go on our web app and it would show them the location of there smart car. 

## Stack
The web app was developed using HTML, CSS, and Javascript. The front end was designed using bootstrap and the back end was designed using python and flask was used to connect both of them. The smart car api was used to recieve the coordinates of ones car. The cars location was displayed to users using three google maps apis. One was a general map showing directions to your car. The other was a streetview image of what is around your car, with microsoft azures computer vision api being used to analyze this photo to give a description of the surroundings. The last google api used was in case the car was not located on a street, so we used the api to get the nearest street location. 

### Role
Role: I set up all the API's and their keys. I also designed and developed the front end of the web app as well as integrated all the google map api's. I helped in the development of the back end as well as integrating flask to connect the front and back end together.
