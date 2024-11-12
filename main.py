import csv
from collections import defaultdict

protocol_mapping = {
    0: "HOPOPT",
    1: "ICMP",
    2: "IGMP",
    3: "GGP",
    4: "IPv4",
    5: "ST",
    6: "TCP",
    7: "CBT",
    8: "EGP",
    9: "IGP",
    10: "BBN-RCC-MON",
    11: "NVP-II",
    12: "PUP",
    13: "ARGUS (deprecated)",
    14: "EMCON",
    15: "XNET",
    16: "CHAOS",
    17: "UDP",
    18: "MUX",
    19: "DCN-MEAS",
    20: "HMP",
    21: "PRM",
    22: "XNS-IDP",
    23: "TRUNK-1",
    24: "TRUNK-2",
    25: "LEAF-1",
    26: "LEAF-2",
    27: "RDP",
    28: "IRTP",
    29: "ISO-TP4",
    30: "NETBLT",
    31: "MFE-NSP",
    32: "MERIT-INP",
    33: "DCCP",
    34: "3PC",
    35: "IDPR",
    36: "XTP",
    37: "DDP",
    38: "IDPR-CMTP",
    39: "TP++",
    40: "IL",
    41: "IPv6",
    42: "SDRP",
    43: "IPv6-Route",
    44: "IPv6-Frag",
    45: "IDRP",
    46: "RSVP",
    47: "GRE",
    48: "DSR",
    49: "BNA",
    50: "ESP",
    51: "AH",
    52: "I-NLSP",
    53: "SWIPE (deprecated)",
    54: "NARP",
    55: "Min-IPv4",
    56: "TLSP",
    57: "SKIP",
    58: "IPv6-ICMP",
    59: "IPv6-NoNxt",
    60: "IPv6-Opts",
    62: "CFTP",
    64: "SAT-EXPAK",
    65: "KRYPTOLAN",
    66: "RVD",
    67: "IPPC",
    69: "SAT-MON",
    70: "VISA",
    71: "IPCV",
    72: "CPNX",
    73: "CPHB",
    74: "WSN",
    75: "PVP",
    76: "BR-SAT-MON",
    77: "SUN-ND",
    78: "WB-MON",
    79: "WB-EXPAK",
    80: "ISO-IP",
    81: "VMTP",
    82: "SECURE-VMTP",
    83: "VINES",
    84: "IPTM",
    85: "NSFNET-IGP",
    86: "DGP",
    87: "TCF",
    88: "EIGRP",
    89: "OSPFIGP",
    90: "Sprite-RPC",
    91: "LARP",
    92: "MTP",
    93: "AX.25",
    94: "IPIP",
    95: "MICP (deprecated)",
    96: "SCC-SP",
    97: "ETHERIP",
    98: "ENCAP",
    100: "GMTP",
    101: "IFMP",
    102: "PNNI",
    103: "PIM",
    104: "ARIS",
    105: "SCPS",
    106: "QNX",
    107: "A/N",
    108: "IPComp",
    109: "SNP",
    110: "Compaq-Peer",
    111: "IPX-in-IP",
    112: "VRRP",
    113: "PGM",
    115: "L2TP",
    116: "DDX",
    117: "IATP",
    118: "STP",
    119: "SRP",
    120: "UTI",
    121: "SMP",
    122: "SM (deprecated)",
    123: "PTP",
    124: "ISIS over IPv4",
    125: "FIRE",
    126: "CRTP",
    127: "CRUDP",
    128: "SSCOPMCE",
    129: "IPLT",
    130: "SPS",
    131: "PIPE",
    132: "SCTP",
    133: "FC",
    134: "RSVP-E2E-IGNORE",
    135: "Mobility Header",
    136: "UDPLite",
    137: "MPLS-in-IP",
    138: "manet",
    139: "HIP",
    140: "Shim6",
    141: "WESP",
    142: "ROHC",
    143: "Ethernet",
    144: "AGGFRAG",
    145: "NSH",
    146: "Homa",
    147: "Reserved",
    253: "Reserved",
    254: "Reserved",
    255: "Reserved",
}


def load_lookup_table(lookup_filename):
    lookup_dict = {}

    with open(lookup_filename, 'r') as lookup_file:
        reader = csv.reader(lookup_file)

        # Skip the top-most header line in the file
        next(reader)
        for row in reader:
            dstport, protocol, tag = row
            dstport = int(dstport)

            # To ensure case-insensitivity, normalize the protocol
            protocol = protocol.lower()
            if (dstport, protocol) not in lookup_dict:
                lookup_dict[(dstport, protocol)] = []
            lookup_dict[(dstport, protocol)].append(tag)
    return lookup_dict


def process_flow_logs(flow_log_filename, lookup):
    tag_counts = defaultdict(int)
    untagged_counts = 0

    portprotocol_counts = defaultdict(int)

    with open(flow_log_filename, 'r') as flow_log_file:
        for line in flow_log_file:
            columns = line.split()
            dstport = int(columns[6])
            protocol_num = int(columns[7])
            protocol = protocol_mapping.get(protocol_num, str(protocol_num)).lower()
            portprotocol_counts[(dstport, protocol)] += 1
            tags = lookup.get((dstport, protocol), [])
            if tags:
                for tag in tags:
                    tag_counts[tag] += 1
            else:
                untagged_counts += 1

    return tag_counts, portprotocol_counts, untagged_counts


def write_output(tag_counts, portprotocol_counts, untagged_counts, output_filename):
    with open(output_filename, 'w') as output_file:
        output_file.write("Tag Counts:\n")
        output_file.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            output_file.write(f"{tag},{count}\n")
        output_file.write(f"Untagged,{untagged_counts}\n")

        output_file.write("\nPort/Protocol Combination Counts:\n")
        output_file.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(portprotocol_counts.items()):
            output_file.write(f"{port},{protocol},{count}\n")


def main():
    # Step 1: Define input and output file paths (adjust as necessary)
    flow_log_filename = 'flow_logs.txt'
    lookup_filename = 'lookup_table.csv'
    output_filename = 'output.txt'

    # Step 2: Load the lookup table from the CSV file into a dictionary
    lookup = load_lookup_table(lookup_filename)

    # Step 3: Process the flow logs and tally the counts
    tag_counts, portprotocol_counts, untagged_counts = process_flow_logs(flow_log_filename, lookup)

    # Step 4: Write the results to the output file
    write_output(tag_counts, portprotocol_counts, untagged_counts, output_filename)


if __name__ == "__main__":
    main()
