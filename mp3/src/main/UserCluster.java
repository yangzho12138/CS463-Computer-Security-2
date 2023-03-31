package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.io.FileNotFoundException;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.Math;

public class UserCluster {
	private Map<Long, List<String>> userMap; // Map a user id to a list of
												// bitcoin addresses
	private Map<String, Long> keyMap; // Map a bitcoin address to a user id

	List<List<String>> records;

	long idx = 0; // user id

	int hash_index = 0;
	int addr_index = 1;
	int val_index  = 2;
	int type_index = 3;
	int column_len = 4;

	public UserCluster() {
		userMap = new HashMap<Long, List<String>>();
		keyMap = new HashMap<String, Long>();
		records = new ArrayList<>();
	}

	/**
	 * Read transactions from file
	 *
	 * @param file
	 * @return true if read succeeds; false otherwise
	 */
	public boolean readTransactions(String file) {
		// TODO implement me
		try(BufferedReader br = new BufferedReader(new FileReader(file))){
			String line;
			String id = "";
			List<String> transactions = new ArrayList<>();
			while((line = br.readLine()) != null){
				String[] r = line.split(" ");
				String transactionId = r[hash_index];
				if(transactionId.equals(id)){
					transactions.add(line);
				}else{
					if(transactions.size() != 0){
						records.add(new ArrayList<>(transactions));
						transactions.clear();
					}
					transactions.add(line);
					id = transactionId;
				}
			}
			records.add(new ArrayList<>(transactions));
			return true;
		}catch (IOException e){
			e.printStackTrace();
		}
		return false;
	}

	/**
	 * Merge addresses based on joint control
	 */
	public void mergeAddresses() {
		// TODO implement me
		for(List<String> transaction : records){
			boolean flag = false;
			long jointUser = 0L;

			for(String t : transaction){
				String[] r = t.split(" ");
				String address = r[addr_index];
				String type = r[type_index];

				if(type.equals("in") && keyMap.containsKey(address)){
					flag = true;
					jointUser = keyMap.get(address);
					break;
				}
			}

//			System.out.println(transaction);
//			System.out.println(flag + " " + jointUser);

			if(flag){ // need to merge
				for(String t : transaction){
					String[] r = t.split(" ");
					String address = r[addr_index];
					String type = r[type_index];

					if(type.equals("in")) {
						if (keyMap.containsKey(address) && keyMap.get(address) != jointUser) {
							long deleteId = keyMap.get(address);
							for (String s : userMap.get(deleteId)) {
								userMap.get(jointUser).add(s);
								keyMap.put(s, jointUser);
							}
							userMap.remove(deleteId);
						} else {
							if (!userMap.get(jointUser).contains(address)) {
								userMap.get(jointUser).add(address);
							}
							keyMap.put(address, jointUser);
						}
					}
					else if(type.equals("out")){
//						System.out.println("test" + address);
//						for(String key : keyMap.keySet()){
//							System.out.print(key + " " + keyMap.get(key) + " | ");
//						}
//						System.out.println("");
						if(!keyMap.containsKey(address)){
							long outId = ++ idx;
							keyMap.put(address, outId);
							List<String> addr = new ArrayList<>();
							addr.add(address);
							userMap.put(outId, addr);
						}
					}
				}
			}else{ // no need to merge - new cluster
				long inId = ++ idx;
				userMap.put(inId, new ArrayList<>());
				for(String t : transaction){
					String[] r = t.split(" ");
					String address = r[addr_index];
					String type = r[type_index];

					if(type.equals("in")) {
						userMap.get(inId).add(address);
						keyMap.put(address, inId);
					}
					else if(type.equals("out")){
						if(!keyMap.containsKey(address)){
							long outId = ++ idx;
							keyMap.put(address, outId);
							List<String> addr = new ArrayList<>();
							addr.add(address);
							userMap.put(outId, addr);
						}
					}
				}
			}

//			for(String t : transaction){
//				String[] r = t.split(" ");
//				String address = r[addr_index];
//				String type = r[type_index];
//
//				if(type.equals("out")){
//					if(!keyMap.containsKey(address)){
//						long outId = ++ idx;
//						keyMap.put(address, outId);
//						List<String> addr = new ArrayList<>();
//						addr.add(address);
//						userMap.put(outId, addr);
//					}
//				}
//			}

//			for(String key : keyMap.keySet()){
//				System.out.print(key + " " + keyMap.get(key) + " | ");
//			}
//			System.out.println("");
//			for(long userId : userMap.keySet()){
//				System.out.print(userId + " " + userMap.get(userId) + " | ");
//			}
//			System.out.println("");
		}

//		for(String key : keyMap.keySet()){
//			System.out.println(keyMap.get(key));
//		}
	}

	/**
	 * Return number of users (i.e., clusters) in the transaction dataset
	 *
	 * @return number of users (i.e., clusters)
	 */
	public int getUserNumber() {
		// TODO implement me
		return userMap.size();
	}

	/**
	 * Return the largest cluster size
	 *
	 * @return size of the largest cluster
	 */
	public int getLargestClusterSize() {
		// TODO implement me
		Set<Long> keySets = userMap.keySet();
		int largestClusterSize = -1;
		Iterator<Long> it = keySets.iterator();
		while(it.hasNext()){
			Long key = it.next();
			largestClusterSize = Math.max(largestClusterSize, userMap.get(key).size());
		}
		return largestClusterSize;
	}

	public boolean writeUserMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (long user : userMap.keySet()) {
				List<String> keys = userMap.get(user);
				w.write(user + " ");
				for (String k : keys) {
					w.write(k + " ");
				}
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing user list!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeKeyMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (String key : keyMap.keySet()) {
				w.write(key + " " + keyMap.get(key) + "\n");
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing key map!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeUserGraph(String txFile, String userGraphFile) {
	     try {
                        BufferedReader r1 = new BufferedReader(new FileReader(txFile));
                        Map<String, Long> txUserMap = new HashMap<String, Long>();
                        String nextLine;
                        while ((nextLine = r1.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r1.close();
                                        return false;
                                }
                                if (s[type_index].equals("in") && !txUserMap.containsKey(s[hash_index])) { // new transaction
                                        Long user;
                                        if ((user=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                System.out.println(nextLine);
                                                r1.close();
                                                return false;
                                        }
                                        txUserMap.put(s[hash_index], user);
                                }
                        }
                        r1.close();

                        BufferedReader r2 = new BufferedReader(new FileReader(txFile));
                        BufferedWriter w = new BufferedWriter(new FileWriter(userGraphFile));
                        while ((nextLine = r2.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r2.close();
                                        w.flush();
                                        w.close();
                                        return false;
                                }
                                if (s[type_index].equals("out")) {
                                        if(txUserMap.get(s[hash_index]) == null) {
                                                System.err.println("Did not find input transaction for Tx: " + s[hash_index]);
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        long inputUser = txUserMap.get(s[hash_index]);
                                        Long outputUser;
                                        if ((outputUser=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        w.write(inputUser + "," + outputUser + "," + s[val_index] + "\n");
                                }
                        }
                        r2.close();
                        w.flush();
                        w.close();
                } catch (IOException e) {
                        e.printStackTrace();
                }
                return true;

	}

	public void analyzeUserGraph(){
		Map<String, Long> senderMap = new HashMap<>();
		Map<String, Long> receiverMap = new HashMap<>();
		Map<String, List<String>> receiverToSenderMap = new HashMap<>();

		String FBIId = null;
		Long maxReceiverValue = Long.MIN_VALUE;

		try(BufferedReader br = new BufferedReader(new FileReader("userGraph.txt"))){
			String line;
			while((line = br.readLine()) != null){
				String[] r = line.split(",");
				String sender = r[0];
				String receiver = r[1];
				String value = r[2];

				List<String> senders = receiverToSenderMap.getOrDefault(receiver, new ArrayList<>());
				senders.add(sender);
				receiverToSenderMap.put(receiver, senders);

				if(senderMap.containsKey(sender)) {
					senderMap.put(sender, senderMap.get(sender) + Long.parseLong(value));
				}else{
					senderMap.put(sender, Long.parseLong(value));
				}

				if(receiverMap.containsKey(receiver)) {
					receiverMap.put(receiver, receiverMap.get(receiver) + Long.parseLong(value));
				}else{
					receiverMap.put(receiver, Long.parseLong(value));
				}

				if(maxReceiverValue < receiverMap.get(receiver)){
					maxReceiverValue = receiverMap.get(receiver);
					FBIId = receiver;
				}
			}

//			System.out.println("FBI ID: " + FBIId);
			List<String> fbiAddr = userMap.get(Long.parseLong(FBIId));
			System.out.println("FBI Address: " + fbiAddr);

			long maxSenderValue = -1L;
			String maxSender = null;
			for(String sender : receiverToSenderMap.get(FBIId)){
				if(maxSenderValue < senderMap.get(sender)){
					maxSenderValue = senderMap.get(sender);
					maxSender = sender;
				}
			}

//			System.out.println("Max Sender: " + maxSender + " with value: " + maxSenderValue);
			List<String> maxSenderAddr = userMap.get(Long.parseLong(maxSender));
			System.out.println("Potential silk road address: " + maxSenderAddr.get(0) + " " + maxSenderAddr.get(1) + " " + maxSenderAddr.get(2));

		}catch (IOException e){
			e.printStackTrace();
		}
	}

}
