# Block Hub - Blockchain Web Application

## Link: https://block-hub-4e06263a7905.herokuapp.com/

### Overview

>Block Hub is a demo of decentralized blockchain web application that allows you to interact with a peer-to-peer network, visualize the current and past states of a blockchain, and modify block data and transactions.

>This project is built using Flask (Python), Bootstrap (CSS), Jinja (templating engine).

## Features

- **Peer Management**: View information about peers in the network and interact with their blockchain data.
- **View Blockchain States**: Display both old and current blockchain data, including block details like Nonce, Previous Hash, Current Hash, and Transactions.
- **Update Block Data**: Modify the data of any block in the blockchain.
- **Update Transaction Data**: Modify transaction amounts and details in the blocks.
- **Real-time Logs**: View logs to monitor real-time events happening in the blockchain.

## Tech Stack

- Backend: **Flask** (Python)
- Frontend: **HTML**, **CSS** (Bootstrap)
- Template Engine: **Jinja**

## Local clone
```
git clone <https://github.com/ChopinF69/Block-Hub.git>
cd Block-Hub
flask run
```

# Tutorial

### 2 options when entering the web site
- Register: After registering, you will receive your password. To get your public address, you first need to retrieve your private address from the server logs. Then, go to the **Get Public Key** section, where you will simply enter the private address you just retrieved from the logs. After that, you'll be able to log in.
- Create a Session: You can create a session with different names, and then you'll need to check the server logs to directly retrieve the public addresses and passwords. You can log in with whichever account you prefer. When creating a session, you'll need to provide a list of names and a difficulty level. The difficulty represents the number of leading zeros required in the hash to demonstrate the **Proof of Work (PoW)** algorithm.

# My account section
- In this section, you can check your public address and balance by default.
- You can add money to your wallet, but note that this is not considered a transaction and will not be stored on the blockchain.
- You can also send money, but first, you will need the public address of the recipient, which you can find in the **All Users** section. Sending money will be considered a transaction and will be stored on the blockchain. Additionally, you can access the **All Network** area to view the transaction.

# All Network
- Here, you will notice a block called the **Genesis Block**, which is the first block in the blockchain. All subsequent blocks will be built upon it.
- You can modify the blocks (either the data or the transaction amount). After modifying, you will see a new layer appear, which will have a **new hash** and **nonce**. A **nonce** is a value that increments sequentially to adjust the difficulty of the network and is used in the hash algorithm.
