from tqdm import tqdm
from pinecone import Pinecone 
from pinecone import ServerlessSpec
from sentence_transformers import SentenceTransformer

def get_embedding_len(model_name):
    # The Embedding model is loaded
    model = SentenceTransformer(model_name)
    return model,model.get_sentence_embedding_dimension()

def get_vectordb_index(pc,index_name,embedding_length, force_create=False):
    if force_create:
        print("Deleting the existing index")
        if pc.has_index(index_name):
            pc.delete_index(index_name)
            
    if not pc.has_index(index_name):
        print("Creating a new index")
        pc.create_index(
            name=index_name,
            dimension=embedding_length,
            metric="cosine",
            spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"),
            deletion_protection="disabled")
    index = pc.Index(index_name)
    
    return index

# Function to check if a specific ID exists in the vector database
def check_id_exists(index, id_to_check):
    response = index.fetch(ids=[id_to_check])
    return id_to_check in response['vectors']

def add_to_vector_db(index,data,model):
    vectors=[]
    print("Encoding any New Resume")
    for group_name, dict_values in tqdm(data.items()):
        if check_id_exists(index, group_name):
            continue
        # Only concerned with the technical skills
        resume= f"education: {dict_values['education']}\nexperience: {dict_values['experience']}\nskills: {dict_values['skills']}\ncourses: {dict_values['courses']}\n"
        # embed the resume 
        resume_embedding = model.encode(resume)
        vectors.append({"id": group_name, "values": resume_embedding})
    
    if len(vectors)>0:
        print("Adding the new resumes to the vector database")
        index.upsert(vectors)

    return index

def search_matched_resumes(job_descriptions,model,index,top_k=5):
    retrievals={}
    for job_name,job_description in job_descriptions.items():
        encoded_jd=model.encode(job_description)
        response=index.query(vector=encoded_jd.tolist(), top_k=top_k)
        top_ids = [match['id'] for match in response['matches']]
        retrievals[job_name]=top_ids
    return retrievals

