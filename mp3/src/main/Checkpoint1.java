package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.IOException;

public class Checkpoint1 {
	Block block;
	// constructor
	public Checkpoint1(){
		String hash = "000000000000000f5795bfe1de0381a44d4d5ea2ad81c21d77f275bffa03e8b3";
		BlockExplorer blockExplorer = new BlockExplorer();
		try{
			this.block = blockExplorer.getBlock(hash);
		}catch (Exception e){
			e.printStackTrace();
		}
	}
	/**
	 * Blocks-Q1: What is the size of this block?
	 *
	 * Hint: Use method getSize() in Block.java
	 *
	 * @return size of the block
	 */
	public long getBlockSize() {
		return block.getSize();
	}

	/**
	 * Blocks-Q2: What is the Hash of the previous block?
	 *
	 * Hint: Use method getPreviousBlockHash() in Block.java
	 *
	 * @return hash of the previous block
	 */
	public String getPrevHash() {
		return block.getPreviousBlockHash();
	}

	/**
	 * Blocks-Q3: How many transactions are included in this block?
	 *
	 * Hint: To get a list of transactions in a block, use method
	 * getTransactions() in Block.java
	 *
	 * @return number of transactions in current block
	 */
	public int getTxCount() {
		return block.getTransactions().size();
	}

	/**
	 * Transactions-Q1: Find the transaction with the most outputs, and list the
	 * Bitcoin addresses of all the outputs.
	 *
	 * Hint: To get the bitcoin address of an Output object, use method
	 * getAddress() in Output.java
	 *
	 * @return list of output addresses
	 */
	public List<String> getOutputAddresses() {
		List<Transaction> transactions = block.getTransactions();
		int outputsNum = 0;
		List<String> target = new ArrayList<>();
		for(Transaction t : transactions){
			List<Output> outputs = t.getOutputs();
			if (outputs.size() > outputsNum){
				outputsNum = outputs.size();
				target.clear();
				for(Output o : outputs){
					target.add(o.getAddress());
				}
			}
		}
		return target;
	}

	/**
	 * Transactions-Q2: Find the transaction with the most inputs, and list the
	 * Bitcoin addresses of the previous outputs linked with these inputs.
	 *
	 * Hint: To get the previous output of an Input object, use method
	 * getPreviousOutput() in Input.java
	 *
	 * @return list of input addresses
	 */
	public List<String> getInputAddresses() {
		List<Transaction> transactions = block.getTransactions();
		int inputsNum = 0;
		List<String> target = new ArrayList<>();
		for(Transaction t : transactions){
			List<Input> inputs = t.getInputs();
			if (inputs.size() > inputsNum){
				inputsNum = inputs.size();
				target.clear();
				for(Input i : inputs){
					if(i.getPreviousOutput() != null){ // generation transaction has no previous outputs
						target.add(i.getPreviousOutput().getAddress());
					}
				}
			}
		}
		return target;
	}

	/**
	 * Transactions-Q3: What is the bitcoin address that has received the
	 * largest amount of Satoshi in a single transaction?
	 *
	 * Hint: To get the number of Satoshi received by an Output object, use
	 * method getValue() in Output.java
	 *
	 * @return the bitcoin address that has received the largest amount of Satoshi
	 */
	public String getLargestRcv() {
		List<Transaction> transactions = block.getTransactions();
		long largestRcv = 0L;
		String target = new String();
		for(Transaction t : transactions){
			List<Output> outputs = t.getOutputs();
			for(Output o : outputs){
				if(largestRcv < o.getValue()){
					largestRcv = o.getValue();
					target = o.getAddress();
				}
			}
		}
		return target;
	}

	/**
	 * Transactions-Q4: How many coinbase transactions are there in this block?
	 *
	 * Hint: In a coinbase transaction, getPreviousOutput() == null --> although this matches with the documentation, the result is wrong.
	 * Even if it's a coinbase transactions, it's not null during my test.
	 * I would recommend another work around that a coinbase transaction should have the sum of getPreviousOutput().getValue() equal to 0 because the total input should be 0.
	 * You can see an example of coinbase transaction here: https://www.blockchain.com/btc/tx/cdab676fe718b5155251f15b275c5f92ad965ee8557270d1eec07ccc42d4aaaf
	 * I'm using Java 1.8.0_242, if anyone made it success with getPreviousOutput() == null, please email me or send a campuswire post. Much appreciated!
	 *
	 * @return number of coin base transactions
	 */
	public int getCoinbaseCount() {
		List<Transaction> transactions = block.getTransactions();
		int coinBaseNum = 0;
		for(Transaction t : transactions){
			List<Input> inputs = t.getInputs();
			for(Input i : inputs){
				if(i.getPreviousOutput().getValue() == 0){
					coinBaseNum ++;
				}
			}
		}
		return coinBaseNum;
	}

	/**
	 * Transactions-Q5: What is the number of Satoshi generated in this block?
	 *
	 * @return number of Satoshi generated
	 */
	public long getSatoshiGen() {
		List<Transaction> transactions = block.getTransactions();
		long sum = 0L;
		for(Transaction t : transactions){
			List<Output> outputs = t.getOutputs();
			for(Output o : outputs){
				sum += o.getValue();
			}
		}
		return sum;
	}

}
