# Inovola Couriers Integration Task

- the core concept of the task is to allow us to register new courier with specifiec data without any integrations code
  so the core proplem was to have dynamic end points and dynamic request objects depends on the logic was implemented in courier api

* so here we have create courier model with domain and different end points attributes to solve the dynamic end points problem
  after that we had to deal with the other big problem

* so we created map fields object and the core concept of it is to map between the our local_name of every field and it's equlaivante field in courier api
  it's also deal with the structure of request body object so we add courier_object_name field to define the parent object of every field

* when we create new courier we define in the request body the object fields it contains all fields belongs to the courier request body in specifec structure
  we define every parent object as an array contain it's fields
  to make it easy to create all courier fields as we decieded before

* sand when we prepare the body object we query on all fields belongs to the courier and start from the main object untill we reach the last nested object

* we used django and rest frame work and requests package to achieve our goal
