package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.FileWriter;
import java.io.IOException;


public class DatasetGenerator {
	String file;

	public DatasetGenerator(String file) {
		this.file = file;
	}

	public boolean writeTransactions() {
		// TODO implement me
		try{
			FileWriter fileWriter = new FileWriter(file, true);

			BlockExplorer blockExplorer = new BlockExplorer();
			List<Block> blocks = new ArrayList<>();
			for(long height = 265852; height <= 266085; height ++) {
				blocks.addAll(blockExplorer.getBlocksAtHeight(height));
			}
			for(Block block : blocks){
				List<Transaction> transactions = block.getTransactions();
				for(Transaction t : transactions){
					String txHash = t.getHash();

					List<Input> inputs = t.getInputs();
					long inputSum = 0;
					for(Input i : inputs){
						inputSum += i.getPreviousOutput().getValue();
					}

					if(inputSum == 0){
						continue;
					}

					for(Input i : inputs){
						// generation transaction has no previous outputs and non-coinbase
						if(i.getPreviousOutput() != null){
							String address = i.getPreviousOutput().getAddress();
							if(address.equals("")){
								continue;
							}
							long value = i.getPreviousOutput().getValue();
							String record = generateInputRecord(txHash, address, value);
							fileWriter.write(record + '\n');
						}
					}

					List<Output> outputs = t.getOutputs();

					for(Output o : outputs){
						String address = o.getAddress();
						if(address.equals("")){
							continue;
						}
						long value = o.getValue();
						String record = generateOutputRecord(txHash, address, value);
						fileWriter.write(record + '\n');
					}
				}
			}
			fileWriter.close();
			return true;
		}catch (Exception e){
			e.printStackTrace();
		}

    	return false;
	}

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Previous output address of the input
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the input
	 */
	private String generateInputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " in";
	}

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Output bitcoin address
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the output
	 */
	private String generateOutputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " out";
	}
}
