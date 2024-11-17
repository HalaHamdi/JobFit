import os 
import sys
import json
import shutil
from dotenv import load_dotenv
from pinecone import Pinecone 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'RAG')))
from RAG import get_embedding_len,get_vectordb_index,add_to_vector_db,search_matched_resumes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Preprocessing')))
from StructureResumes import load_structured_resumes,structure_resumes


def get_database(model_name='multi-qa-MiniLM-L6-cos-v1', index_name="job-fit-ai"): 
    
    load_dotenv()
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
    pc=Pinecone(api_key=pinecone_api_key)
    model, embedding_length=get_embedding_len(model_name)
    index=get_vectordb_index(pc, index_name,embedding_length)
    files_names = [i for i in index.list()][0]
    return model,index,files_names
    
def record_exists(file_name, files_names):
    #return True if file_name exists in the database otherwise False
    return file_name in files_names
    
def ingestion_pipeline(uploaded_files):
    structured_resumes_path='../DataSet/structured_resumes.json'
    processed_resumes = load_structured_resumes(structured_resumes_path)
    processed_resumes_list_path='../Preprocessing/processed_resumes.txt'
    unprocessed_resumes_path='./tmp'
    
    for file in uploaded_files:
        resume_name, extension = os.path.splitext(file.name)
        # if the resume needs the pre-processing pipeline (i.e. parsing & structuring)
        if resume_name not in processed_resumes:
            if not os.path.exists(unprocessed_resumes_path):
                os.makedirs(unprocessed_resumes_path)
            tmp_location = os.path.join(unprocessed_resumes_path+"/", file.name)
            with open(tmp_location, 'wb') as f:
                f.write(file.getbuffer())
                
    # delete the file after processing
    if os.path.exists(unprocessed_resumes_path):
        # any unprocessed resumes need to be structured
        structure_resumes(unprocessed_resumes_path,processed_resumes_list_path,structured_resumes_path)  
        shutil.rmtree(unprocessed_resumes_path)
    
    #read again the processed resumes after structuring the unprocessed resumes
    processed_resumes = load_structured_resumes(structured_resumes_path)
    # add key value pairs to the data dictionary using a python dictionary comprehension
    data = {os.path.splitext(file.name)[0]:processed_resumes[os.path.splitext(file.name)[0]] for file in uploaded_files if os.path.splitext(file.name)[0] in processed_resumes}
        
    return data

def match(job_description,uploaded_files,top_k,st):
    print("--------------------------------------------------")
    bar= st.empty()
    with bar.status("In progress...",expanded=True) as status:
        # Any new resume needs pre-processing
        # returns the data needed to be added to the vector database
        st.write("Processing resumes...")
        data=ingestion_pipeline(uploaded_files)
        model_name = 'multi-qa-MiniLM-L6-cos-v1'
        model, embedding_length=get_embedding_len(model_name)
        
        st.write("Preparing the database...")
        load_dotenv()
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
        
        index_name = "job-fit-ai"
        pc=Pinecone(api_key=pinecone_api_key)
        
        index=get_vectordb_index(pc, index_name,embedding_length, force_create=False)
        index=add_to_vector_db(index,data,model)  # embed the resumes and add them to the pinecone database
        
        st.write("Searching Best Resumes...")
        encoded_jd=model.encode(job_description)
        response=index.query(vector=encoded_jd.tolist(), top_k=top_k)
        
        top_resumes_names = {match['id']+'.pdf': match['score'] for match in response['matches']}
    bar.empty()
    return [(resume, top_resumes_names[resume.name]) for resume in uploaded_files if resume.name in top_resumes_names]
    
    

    
             
