import streamlit as st 
import pickle 
from filter import * 

@st.experimental_memo
def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

@st.experimental_memo
def load_objects(): 
#    obj = load("filtered.obj")
    raw_meta = load("reorganized_meta.obj")
    return raw_meta


reorganize_meta = load_objects()
st.title("GEO Search *beta*")
#st.sidebar.subheader("The following search tool parses GEO series 14-19 finding matches using keywords for tissue (e.g. PBMC) and technology (such as scRNAseq). The tool outputs a title, summary, and overall design of matching datasets. Clicking the button for each dataset will add the dataset to the cart.")


#@st.experimental_memo
def _search(input, technology, _reorganized_meta):

    for i in range(0, len(reorganize_meta)):
        o = reorganize_meta[i]
        o.index = None 

    for i, s in enumerate(input):
        input[i] = s.lower().strip()


    for i, s in enumerate(technology):
        technology[i] = s.lower().strip()
        
    hits = 0
    
    filtered = [] 
    for i in range(0, len(reorganize_meta)):
        obj = reorganize_meta[i]

        set_title = set(obj.supplementary_information['title_lower_list'])
        set_summary = set(obj.supplementary_information['summary_list'])
        set_overall_design = set(obj.supplementary_information['overall_design_lower_list'])
        set_technology = set(technology)
        for items in input:
            if items in set_title  or items in set_overall_design or items in set_overall_design or items in obj.author: 
                if (set_technology & set_title) or (set_technology & set_summary) or (set_technology & set_overall_design):
                    if obj.index == None:
                        filtered.append(obj)
                        hits += 1
                        reorganize_meta[i].index = i
                    else: 
                        continue
                        
    return filtered

#technology = [ 'chromium', '10x', "scRNAseq", "single-cell RNA-seq", "scRNA-seq", "scRNA", "single cell RNA-seq", "single cell RNAseq", "single cell"]
#tissue = ["pbmc", "peripheral blood" ,"blood"]
#chromium, 10x, scRNAseq, single-cell RNA-seq, scRNA-seq, scRNA, single cell RNA-seq, single cell RNAseq, single cell
#pbmc, peripheral blood, blood
# obj = (search(['pbmc', 'peripheral blood', 'blood'], technology))

saved = []
if 'saved' not in st.session_state:
    st.session_state.saved = saved

if 'reoganized_meta' not in st.session_state:
    st.session_state.reorganized_meta = reorganize_meta

if 'initial_input' not in st.session_state:
    st.session_state.initial_input = 0

if 'total_studies' not in st.session_state:
    st.session_state.total_studies =0
if 'meeting_search' not in st.session_state:
    st.session_state.meeting_search =0


tissue_input = st.sidebar.text_input("Keywords (e.g tissue), please input as a comma seperated list")
#tissue_input = ["ALS"]
technology_input = st.sidebar.text_input("Platform Keywords (e.g scRNAseq, single cell RNAseq), please input as a comma separated list")
#technology_input = ["10X"]
search_reply = st.sidebar.button("Search!")

if(st.session_state.initial_input == 0):   
    st.balloons()
st.session_state.initial_input = 1


@st.experimental_memo
def trim_meta(_meta): 
    trimmed_reorganized_meta = []
    for i in range(0, len(_meta)):
        obj = _meta[i]
        trimmed_reorganized_meta.append({"title" : obj.title,'accession' : obj.accession, 'samples' : obj.number_of_samples, "summary" : obj.summary, "overall_design" : obj.overall_design} )

    if 'trimmed_meta' not in st.session_state:
        st.session_state.trimmed_meta= trimmed_reorganized_meta


if len(tissue_input) != 0 and len(technology_input) != 0 and st.session_state.initial_input == 1: 


    tissue_input = tissue_input.split(",")


    technology_input = technology_input.split(",")

    search_results = _search(input = tissue_input, technology = technology_input, _reorganized_meta = st.session_state.reorganized_meta)
    # trim_meta(obj)
    
    st.session_state.meeting_search = len(search_results)
    for i in range(0, len(search_results)):
        obj = search_results[i]
        button = obj.accession
        reply = st.button(button)

        st.write("**" +obj.title + "**")
        st.write("*Number of Samples: " + str(obj.number_of_samples) + "*")
        st.write(obj.summary)
        st.write(obj.overall_design)

            
        if reply:
            if obj not in st.session_state.saved:
                st.session_state.saved.append(obj)
            else:
                st.warning('Already Saved!')

    st.sidebar.metric("Total Studies Meeting Search", st.session_state.meeting_search)
    st.sidebar.metric("Studies in Cart", len(st.session_state.saved))
    
st.sidebar.metric("Studies in Database", len(st.session_state.reorganized_meta))
    # if len(st.session_state.saved) != 0:
    #     view_cart = st.sidebar.button("View Cart")
    #     if view_cart:   
    #         for i in range(0, len(st.session_state.saved)):
    #             st.sidebar.write("**" + st.session_state.saved[i].accession + "**")
    #             st.sidebar.write(st.session_state.saved[i].title)







