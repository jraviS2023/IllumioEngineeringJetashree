# IllumioEngineeringJetashree

## Compilation/Running Instructions:

1. <b> Prepare the Input File: </b> Ensure you have your flow_logs.txt file ready. This file contains the flow log data that will be processed by the script [NOTE: It is included in the project already!]
2. <b> Run the Script: </b> After installing the dependencies and preparing your input file, you can run the main Python script with Python 3:

```python3 main.py```

## Assumptions:

1. <b> Flow log file format: </b> The flow log data will follow the AWS VPC flow log format, version 2, as outlined [here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields). Expect the standard set of data like srcaddr, dstaddr, srcport, and dstport—you know, all the typical flow log fun!

```<version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status>```

2. <b> Lookup table format: </b> The lookup table will be your trusty CSV file, where each row has a combination of `dstport`, `protocol`, and the corresponding `tag`. It’s like your flow log GPS for tag mapping.
3. <b> Case-insensitivity: </b> The algorithm is all about inclusivity here. Both port/protocol matches and tag mappings are case-insensitive. Whether you shout your protocol as TCP or whisper it as tcp, the algorithm has got your back.
4. <b> Performance considerations: </b> The solution is robust enough to handle flow log files up to 10MB in size. And your lookup table? It can have up to 10,000 mappings—think of it like a treasure chest full of tags waiting to be discovered.

## Algorithm Steps:

1. <b> Load the Lookup Table: </b> Start by loading the lookup table (CSV) into memory. Each line gets converted into a `(dstport, protocol)` key, which then maps to a list of tags. We keep it nice and tidy, with all ports and protocols converted to lowercase for that extra touch of class. Additionally, the protocol number from the flow log is mapped to its corresponding protocol name (e.g., `6` becomes `tcp`, `17` becomes `udp`, etc.) for readability and consistency.
2. <b> Process the Flow Logs: </b> Next, we go line by line through the flow log file. Each log entry contains a `dstport` and a `protocol number`. The protocol number is first mapped to its name using the protocol mapping (e.g., `6` becomes `tcp`). We then compare the `(dstport, protocol)` pair against our lookup table. If we find a match, we tally the tags. If not, we simply count it as “Untagged.” Simple but effective!
3. <b> Count and Tally: </b> For each tag match, we count how often it appears. We also keep track of how often each port/protocol combination shows up. This way, you get both the frequency of specific tags and the popularity of port/protocol combos.
4. <b> Write the Output: </b> The final step is writing the results into an output file. You’ll get two major section;
- <b> Tag Counts: </b> How many times each tag appeared (including a count of "Untagged").
- <b> Port/Protocol Counts: </b> A breakdown of how often each port/protocol combination occurred.

## Design Decisions:

1. <b> Case-Insensitive Matching: </b> Case sensitivity is so last season. By normalizing both the ports and protocols to lowercase, we ensure we don't miss a match because of case mismatches. We’re all about simplicity and inclusivity in the algorithm.
2. <b> Efficient Data Structures: </b> We use dictionaries (specifically `defaultdict`) to store counts of tags and port/protocol combinations. This makes the code efficient and keeps it clean. It's like having your own personal assistant that tracks everything automatically!
3. <b> Scalability: </b> The solution was designed to scale up to 10MB flow logs and 10,000 mappings in the lookup table. It’s fast, efficient, and doesn’t break a sweat under pressure.

## Future Improvements:

1. <b> Enhanced Lookup Performance: </b> As the number of port/protocol combinations increases, we might explore optimizations like using more advanced data structures or even caching frequently used combinations.
2. <b> Support for Multiple Flow Log Formats: </b> While we currently handle AWS VPC logs, it’d be nice to extend support to other cloud providers or custom log formats. The more, the merrier!
3. <b> Parallel Processing for Huge Files: </b> As log sizes get even larger (think 100MB+), we could introduce parallel processing to handle the file in chunks. No more waiting around for the magic to happen—speed is everything!

