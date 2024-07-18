import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict

def construct_graph(hierarchy_str):
    G = nx.DiGraph()
    levels = {}
    lines = hierarchy_str.strip().split("\n")
    pattern = re.compile(r"(\d+) ([^\s]+)")
    not_found_nodes = set()

    for line in lines:
        if "Cannot find" in line:
            parts = line.split()
            not_found_nodes.add(parts[3])
            not_found_nodes.add(parts[6])
            continue
        if "->" in line:
            parent, children_str = line.split(" -> ")
            parent_match = pattern.match(parent)
            if parent_match:
                parent_level = int(parent_match.group(1))
                parent_node = parent_match.group(2)
                levels[parent_node] = parent_level

                children = pattern.findall(children_str)
                for child_level, child_node in children:
                    child_level = int(child_level)
                    levels[child_node] = child_level
                    G.add_edge(parent_node, child_node)
            else:
                print(f"Skipping malformed parent entry: '{parent}'")
    return G, levels, not_found_nodes

def draw_graph(G, levels, not_found_nodes):
    pos = {}
    level_positions = defaultdict(int)

    # Assign positions for all nodes
    for node, level in levels.items():
        pos[node] = (level_positions[level], -level)
        level_positions[level] += 1

    plt.figure(figsize=(50, 27))

    # Separate nodes into two lists
    found_nodes = [node for node in G.nodes() if node not in not_found_nodes]
    not_found_nodes_list = list(not_found_nodes)

    # Print debugging information
    print(f"Found nodes: {found_nodes}")
    print(f"Not found nodes: {not_found_nodes_list}")

    # Draw edges first to ensure they are behind the nodes
    nx.draw_networkx_edges(G, pos, arrowsize=20)

    # Draw found nodes
    nx.draw_networkx_nodes(G, pos, nodelist=found_nodes, node_color="lightblue", node_size=1000)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in found_nodes}, font_size=10, font_weight="bold")

    # Draw not found nodes last
    nx.draw_networkx_nodes(G, pos, nodelist=not_found_nodes_list, node_color="red", node_size=1000)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in not_found_nodes_list}, font_size=10, font_weight="bold")

    plt.show()


# Example usage
hierarchy_str = r"""
Cannot find: 2 ?Vdz{ -> 1 CNR~[
1 CNR~[ -> 0 CLm~{
2 ?Vdz{ -> 1 ?Z\z{ 1 ?lv]{

1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 2 gCm|{ -> 1 CYr~s
1 CYr~s -> 0 Baj~{
2 gCm|{ -> 1 BIM~{ 1 EI^Z{

1 BIM~{ -> 0 CLm~{
1 EI^Z{ -> 0 CLm~{


Cannot find: 2 EHLz{ -> 1 CYr~s
1 CYr~s -> 0 Baj~{
2 EHLz{ -> 1 @rTz{ 1 BIM~{ 1 AMmz{

1 @rTz{ -> 0 @qz}{
1 BIM~{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{


Cannot find: 3 ?Yzuk -> 2 AMnmw
2 AMnmw -> 1 CNR~[
2 AMnmw -> 1 CLm~w
3 ?Yzuk -> 2 ?lq~[ 2 ?uvZw 2 ?Vdz{

2 ?lq~[ -> 1 C]r]{ 1 ?Z\z{ 1 ?lv]{
2 ?uvZw -> 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 C]r]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 GQX~k -> 2 GqX~k
2 GqX~k -> 1 _hX~{
2 GqX~k -> 1 CNR~[
2 GqX~k -> 1 CLm~w
3 GQX~k -> 2 ?Xu|{ 2 ?Vdz{ 2 ?urn[

2 ?Xu|{ -> 1 @rTz{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{
2 ?urn[ -> 1 ?lv]{

1 @rTz{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?czn[ -> 2 AS|^k
2 AS|^k -> 1 QhX~k
2 AS|^k -> 1 @oy~{
2 AS|^k -> 1 CLm~w
3 ?czn[ -> 2 ?W}|{ 2 ?lq~[ 2 ?Vdz{

2 ?W}|{ -> 1 ?S~^{ 1 AMmz{ 1 _L\~[ 1 ?Z\z{
2 ?lq~[ -> 1 C]r]{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 ?S~^{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 _L\~[ -> 0 @qz}{ 0 CLm~{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 C]r]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?tdj{ -> 2 @]VM{
2 @]VM{ -> 1 EI^Z{
2 @]VM{ -> 1 CNR~[
3 ?tdj{ -> 2 ?urZ{ 2 ?Vdz{ 2 ?urn[

2 ?urZ{ -> 1 @lu]{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{
2 ?urn[ -> 1 ?lv]{

1 @lu]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 IAkz{ -> 2 _czn[
2 _czn[ -> 1 C]r]{
2 _czn[ -> 1 _L\~[
2 _czn[ -> 1 CNR~[
3 IAkz{ -> 2 ?Vdz{ 2 ?urn[

2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{
2 ?urn[ -> 1 ?lv]{

1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?NRv[ -> 2 DQZ^s
2 DQZ^s -> 1 Gdt~w
2 DQZ^s -> 1 DPk~{
2 DQZ^s -> 1 CNR~[
3 ?NRv[ -> 2 ?lq~[ 2 ?Vdz{ 2 ?urn[

2 ?lq~[ -> 1 C]r]{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{
2 ?urn[ -> 1 ?lv]{

1 C]r]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?K}n[ -> 2 @S}^k
2 @S}^k -> 1 QMi~k
2 @S}^k -> 1 @oy~{
2 @S}^k -> 1 CNR~[
3 ?K}n[ -> 2 ?K~]{ 2 ?lq~[ 2 ?Vdz{

2 ?K~]{ -> 1 _K~]{ 1 ?Z\z{
2 ?lq~[ -> 1 C]r]{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 _K~]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 C]r]{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?ddz{ -> 2 _ddz{
2 _ddz{ -> 1 BIM~{
2 _ddz{ -> 1 CNR~[
3 ?ddz{ -> 2 ?dlz{ 2 ?Vdz{

2 ?dlz{ -> 1 AUlz{ 1 ?Z\z{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 AUlz{ -> 0 Qh\z{ 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?Fdz{ -> 2 _Fdz{
2 _Fdz{ -> 1 _NTz{
2 _Fdz{ -> 1 @bJ~{
2 _Fdz{ -> 1 CNR~[
3 ?Fdz{ -> 2 ?Iz}{ 2 ?Vdz{

2 ?Iz}{ -> 1 AJ\z{ 1 ?Z\z{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 AJ\z{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?Wu|{ -> 2 ?Vdz{
2 ?Vdz{ -> 1 @FJ~{
2 ?Vdz{ -> 1 CNR~[
3 ?Wu|{ -> 2 ?W}|{ 2 ?Xu|{ 2 ?Vdz{

2 ?W}|{ -> 1 ?S~^{ 1 AMmz{ 1 _L\~[ 1 ?Z\z{
2 ?Xu|{ -> 1 @rTz{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 ?S~^{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 _L\~[ -> 0 @qz}{ 0 CLm~{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 @rTz{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?SvZ{ -> 2 ?Vdz{
2 ?Vdz{ -> 1 @FJ~{
2 ?Vdz{ -> 1 CNR~[
3 ?SvZ{ -> 2 ?S~Z{ 2 ?Vdz{

2 ?S~Z{ -> 1 ?S~^{ 1 CTlz{ 1 ?Z\z{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 ?S~^{ -> 0 CLm~{
1 CTlz{ -> 0 @qz}{ 0 CLm~{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 ?Iuz{ -> 2 ?Vdz{
2 ?Vdz{ -> 1 @FJ~{
2 ?Vdz{ -> 1 CNR~[
3 ?Iuz{ -> 2 ?Iz}{ 2 ?Xu|{ 2 ?Vdz{

2 ?Iz}{ -> 1 AJ\z{ 1 ?Z\z{
2 ?Xu|{ -> 1 @rTz{ 1 ?Z\z{ 1 ?lv]{
2 ?Vdz{ -> 1 ?Z\z{ 1 AjR|{ 1 ?lv]{

1 AJ\z{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 @rTz{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 ?lv]{ -> 0 ?z\z{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AjR|{ -> 0 Baj~{ 0 @qz}{
1 ?lv]{ -> 0 ?z\z{


Cannot find: 3 @RH~s -> 2 @oy~k
2 @oy~k -> 1 QhX~k
2 @oy~k -> 1 @oy~{
2 @oy~k -> 1 EI^Z{
3 @RH~s -> 2 @O}~w 2 AjP~s

2 @O}~w -> 1 Gdt~w 1 @P\~{ 1 CLm~w
2 AjP~s -> 1 DPk~{ 1 CYr~s 1 CLm~w

1 Gdt~w -> 0 Baj~{
1 @P\~{ -> 0 Baj~{ 0 CLm~{
1 CLm~w -> 0 CLm~{
1 DPk~{ -> 0 Baj~{ 0 CLm~{
1 CYr~s -> 0 Baj~{
1 CLm~w -> 0 CLm~{


Cannot find: 3 ?FLz{ -> 2 GDm|{
2 GDm|{ -> 1 _NTz{
2 GDm|{ -> 1 @P\~{
2 GDm|{ -> 1 EI^Z{
3 ?FLz{ -> 2 ?W}|{ 2 ?Iz}{

2 ?W}|{ -> 1 ?S~^{ 1 AMmz{ 1 _L\~[ 1 ?Z\z{
2 ?Iz}{ -> 1 AJ\z{ 1 ?Z\z{

1 ?S~^{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 _L\~[ -> 0 @qz}{ 0 CLm~{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{
1 AJ\z{ -> 0 @qz}{
1 ?Z\z{ -> 0 @qz}{ 0 ?z\z{


Cannot find: 3 GDk|{ -> 2 AL\^[
2 AL\^[ -> 1 QMi}{
2 AL\^[ -> 1 AUlz{
2 AL\^[ -> 1 @oy~{
2 AL\^[ -> 1 _L\~[
3 GDk|{ -> 2 GDm|{ 2 EH\^[ 2 EIZZ{

2 GDm|{ -> 1 _NTz{ 1 @P\~{ 1 EI^Z{
2 EH\^[ -> 1 KQ\z{ 1 DPk~{ 1 J`\\{ 1 EI^Z{
2 EIZZ{ -> 1 Ahtz{ 1 DPk~{ 1 Aejz{ 1 J`\\{ 1 EI^Z{

1 _NTz{ -> 0 Baj~{
1 @P\~{ -> 0 Baj~{ 0 CLm~{
1 EI^Z{ -> 0 CLm~{
1 KQ\z{ -> 0 Qh\z{ 0 Baj~{
1 DPk~{ -> 0 Baj~{ 0 CLm~{
1 J`\\{ -> 0 Qh\z{
1 EI^Z{ -> 0 CLm~{
1 Ahtz{ -> 0 Qh\z{ 0 Baj~{
1 DPk~{ -> 0 Baj~{ 0 CLm~{
1 Aejz{ -> 0 CLm~{
1 J`\\{ -> 0 Qh\z{
1 EI^Z{ -> 0 CLm~{


Cannot find: 3 gCm|w -> 2 CYr~o
2 CYr~o -> 1 CYr~s
2 CYr~o -> 1 Gdt~w
3 gCm|w -> 2 gCm|{ 2 BIM~w 2 Ajp}s

2 gCm|{ -> 1 BIM~{ 1 EI^Z{
2 BIM~w -> 1 BIM~{ 1 CLm~w
2 Ajp}s -> 1 EI^Z{ 1 CLm~w

1 BIM~{ -> 0 CLm~{
1 EI^Z{ -> 0 CLm~{
1 BIM~{ -> 0 CLm~{
1 CLm~w -> 0 CLm~{
1 EI^Z{ -> 0 CLm~{
1 CLm~w -> 0 CLm~{


Cannot find: 3 EHLzw -> 2 CYr~o
2 CYr~o -> 1 CYr~s
2 CYr~o -> 1 Gdt~w
3 EHLzw -> 2 @rTzw 2 EHLz{ 2 BIM~w 2 Aszl[

2 @rTzw -> 1 @lu]{ 1 @rTz{
2 EHLz{ -> 1 @rTz{ 1 BIM~{ 1 AMmz{
2 BIM~w -> 1 BIM~{ 1 CLm~w
2 Aszl[ -> 1 @lu]{ 1 AMmz{ 1 CLm~w

1 @lu]{ -> 0 @qz}{
1 @rTz{ -> 0 @qz}{
1 @rTz{ -> 0 @qz}{
1 BIM~{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 BIM~{ -> 0 CLm~{
1 CLm~w -> 0 CLm~{
1 @lu]{ -> 0 @qz}{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 CLm~w -> 0 CLm~{


Cannot find: 3 A_j|{ -> 2 gCm|{
2 gCm|{ -> 1 PO]~{
2 gCm|{ -> 1 CYr~s
3 A_j|{ -> 2 EHLz{ 2 CPlz{ 2 AIZ|{ 2 GFJ|{ 2 @`J~{ 2 gCm|{

2 EHLz{ -> 1 @rTz{ 1 BIM~{ 1 AMmz{
2 CPlz{ -> 1 Ahtz{ 1 KQ\z{ 1 @bJ~{ 1 CTlz{ 1 _L\~[
2 AIZ|{ -> 1 AJ\z{ 1 AIZ~{ 1 CTlz{ 1 AMmz{
2 GFJ|{ -> 1 AJ\z{ 1 @rTz{ 1 _L\~[ 1 AIZ~{ 1 EI^Z{
2 @`J~{ -> 1 PDJ~{ 1 AIZ~{ 1 @bJ~{ 1 BIM~{
2 gCm|{ -> 1 BIM~{ 1 EI^Z{

1 @rTz{ -> 0 @qz}{
1 BIM~{ -> 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 Ahtz{ -> 0 Qh\z{ 0 Baj~{
1 KQ\z{ -> 0 Qh\z{ 0 Baj~{
1 @bJ~{ -> 0 Baj~{ 0 CLm~{
1 CTlz{ -> 0 @qz}{ 0 CLm~{
1 _L\~[ -> 0 @qz}{ 0 CLm~{
1 AJ\z{ -> 0 @qz}{
1 AIZ~{ -> 0 CLm~{
1 CTlz{ -> 0 @qz}{ 0 CLm~{
1 AMmz{ -> 0 @qz}{ 0 CLm~{
1 AJ\z{ -> 0 @qz}{
1 @rTz{ -> 0 @qz}{
1 _L\~[ -> 0 @qz}{ 0 CLm~{
1 AIZ~{ -> 0 CLm~{
1 EI^Z{ -> 0 CLm~{
1 PDJ~{ -> 0 Baj~{
1 AIZ~{ -> 0 CLm~{
1 @bJ~{ -> 0 Baj~{ 0 CLm~{
1 BIM~{ -> 0 CLm~{
1 BIM~{ -> 0 CLm~{
1 EI^Z{ -> 0 CLm~{
"""

temp_str = r"""
Cannot find: 2 ?Vdz{ -> 1 CNR~[
"""
G, levels, not_found_nodes = construct_graph(hierarchy_str)
draw_graph(G, levels, not_found_nodes)
