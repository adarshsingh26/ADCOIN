
# ADCOIN

[![GitHub](https://img.shields.io/badge/--181717?logo=github&logoColor=ffffff)](https://github.com/adarshsingh26)
[![Python](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8%7C3.9-blue)](https://www.python.org/) 
[![MIT License](https://img.shields.io/badge/license-MIT-blueviolet)](https://github.com/adarshsingh26/ADCOIN/blob/master/LICENSE) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/adarshsingh26/ADCOIN/graphs/commit-activity)



Adcoin is a `cryptocurrency` built from scratch by `implementing a blockchain` with 
proof of work consensus algorithm.
User can use the webapp to `send/recieve crypto coins` from other users on the network. 
User can manually enter payment data or scan QRCode to make payments directly to another user on network.

## Table Of Contents

 - [Demo (Coming soon)]() 
 - [Problem and Solution](#problem-and-solution)
 - [Tech Stack](#tech-stack)
 - [Common Terms](#common-terms) 
 - [Features](#features)
 - [Repo contents](#repo-contents)
 - [Installation](#installation) 
 - [Overview of how the system works](#overview-of-how-the-system-works)
 - [Tests](#tests)

## Problem and Solution
**Problem** in existing systems:
- `Centralization:` An online bank is only as good as your internet connection. If there’s a power outage, or if servers go down, or if the server is attacked by some attacker you might not have any access to your account when in need. 
- `Trust issues:` You need to trust the bank and their employees that they won’t commit any fraud and your money would be safe, there is no trust build into the system, and this is an issue as various frauds are committed.
- `Identity Theft:` When you give your credit card to a merchant, or you share your personal information and even with the bank by trusting them you give him or her access to your full credit line, so there is a risk of fraud and identity theft.
- `etc`

**Solution** provided:
- Very low cost of cross border transactions than traditional banking system(**40–80% reduction in transaction costs**). [Source Delloite ppt](https://www2.deloitte.com/content/dam/Deloitte/global/Documents/grid/cross-border-payments.pdf).
- Transactions are processed quicker and cheaper than standard systems.
- A peer-to-peer network that removes the need for trusting third parties.
- It is not controlled by one single company and it has no single point of failure.
- You don't have to trust a third party: a bank, a person, or any intermediary that could operate between you and your transactions.

- `Hence it provides autonomy,privacy and saves cost.`
## Tech Stack
- **Backend:** `Python 3.7` `Flask` 
- **Frontend:** `Html` `Bootstrap` `Vue.js` 
- **Testing:** `Postman`

## Common Terms
- `Blockchain:` It is an immutable ledger made up of blocks which contains data(transactions in our case) and this blocks are linked together and secured using cryptography. 
- `Mempool:` Staging area where all the valid transactions wait to be confirmed by the network.
- `Mining:` It is the process by which new Adcoin are entered into circulation. Miners receive Adcoin as a reward for completing "blocks" of verified transactions, which are added to the blockchain.
- `Consensus Algorithm:` It is a process used to achieve agreement on a single data value among distributed processes or systems.Our blockchain will use the Proof of Work consensus algorithm.

## Features
A web Ui is provided, so users can interact with the system. User can
- Create,load or delete an existing wallet.
- Send and receive coins from other users.
- View wallet balance.
- View the blockchain.
- View the mempool.
- Can also participate in mining.
It is a decentralized system.Nodes are connected with each other(peer to peer connection) so there is no server involved in between.


## Repo contents
- `blockchain.py` - This is the code which handles the blockchain.Contains functions for adding transaction to mempool, mining block,adding the block to blockchain,resolving conflict using consensus algorithm,etc.
- `node.py` - Contains HTTP API endpoints which enables nodes to broadcast data to other nodes and recieve data from them.
- `block.py` - Contains the block structure like what attributes a block has.
- `transaction.py` - Contains the transaction structure like what attributes a transaction has.
- `wallet.py` - Contains the wallet structure and methods such as create,load or delete a wallet,etc.
- `node.html` - Contains the UI for the web app .It is a single page web app.
- `style.css` - Contains the style for the web app.

## Installation
Now lets get started by setting up the web app on our machine.
1) Clone repo
```
git clone https://github.com/adarshsingh26/ADCOIN.git
```
2) Download and install Python 3.7 or upper version and make sure to add the path of python into environament variable.

3) Lets create the virtual environment.
```
python -m venv c:\path\to\ADCOIN\myenv
```

4) Change directory to root of project and activate the virtual environment.
```
cd c:\users\ADCOIN
myenv\Scripts\activate
```

5) Install the modules required to run the project
- Navigate to root of project
- ``` pip install requirements.txt ```

6) Now we could run the node.py to run the web app become a node on the network.
```
python node.py -p 5000 (-p  is for the port no)
```

## Overview of how the system works
![Blockchain](https://user-images.githubusercontent.com/84853854/133923193-ca1eda3a-785f-4322-8c22-71073b3f20da.png)

1) If some person wants to send money a new `transaction` is created and it is `signed` by the user `private key` and the transaction is `broadcasted` to other nodes.

2) The nodes on the network work together to `verify transactions` and are rewarded with the coins, a process known as `mining`.

3) Once a transaction is verified by the network, the transaction is placed in a `block` and `added to blockchain`.New transaction blocks are placed in order just after the previous block of transactions.

4) Each node maintains a `copy` of the blockchain.

5) Whichever `node` mines the block first `broadcasts` that `block` to the other nodes.

6) Nodes `verify the block` and then adds it to their local blockchain.

7) And this complete steps results into a `succesfull transaction` on the network.

8) Blockchain is completely `decentralized` so conflicts can happen when broadcasting as some request may reach faster to some nodes while at some cases it may take time.

9) Consensus algorithm is implemented to resolve this conflict so basically this algorithm suggest that that the `majority of nodes(>50%) that have the longest chain will win` and that blockchain will be accepted by all other nodes on the network.

`Note:` As I am building a cryptocurrency the data stored inside the blockchain is transaction, but it could be `any kind of data` as per your application needs.

## Tests
| Test id  | Test Description  | Test Steps | Results
| --- | --- | --- | --- |
| `1` | Recipient address | Enters **public key** of recipient | Address **accepted**
| `2` | Recipient address | Enters *wrong recipient address* | Address **not accepted**
| `3` | Amount of coins | Enters **negative** number of coins | Amount **not accepted**
| `4` | Amount of coins | Enters **positive** number of coins | Amount **accepted**
| `5` | Delete Wallet | Try deleting wallet if it dosen’t exist | Operation **not allowed**
| `6` | Delete Wallet | Deleting wallet when it exists | Operation **allowed**
| `7` | Generate QR code | Enter amount negative or no input | Operation **not allowed**
| `8` | Generate QR code | Enter positive amount  | Operation **allowed**
| `9` | Scan QR Code | Scanning invalid QR code  | Operation **not allowed**
| `10` | Scan QR Code | Scanning valid QR code  | Operation **allowed**

``` HTTP API Endpoints in node.py were tested using Postman Tool ```
