# SDLE First Assignment

SDLE First Assignment of group T3G13.

Group members:

- Tiago Antunes (up201805327@edu.fc.up.pt)
- Tomás Fidalgo (up201906743@fe.up.pt)
- Vasco Alves (up201808031@fe.up.pt)
----

## How to run

1. Install pyzmq library

        pip install pyzmq

2. Clone the repository and change to repository

        git clone https://git.fe.up.pt/sdle/2022/t3/g13/proj1.git
        cd proj1

3. Run the server

        pyhton src/server.py

4. Open a new terminal and run subscriber with id as argument

        python src/subscriber.py <id>

5. Open a new terminal and run publisher
        
        python src/publisher.py