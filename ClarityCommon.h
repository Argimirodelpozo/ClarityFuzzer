#include <vector>
#include <unordered_map>
#include <map>
#include <string>

#pragma once

using namespace std;

//Type definitions
enum types{INT, UINT, BOOL, PRINCIPAL, BUFFER, STRING_ASCII, STRING_UTF8, LIST, TUPLE, OPTION, RESPONSE, NONE};

struct clarity_type
{
    types type;

    int64_t clar_int = 0;
    uint64_t clar_uint = 0;
    bool clar_bool = false;
    string clar_principal;
    string clar_string_ascii;
    string clar_string_utf8;
    vector<clarity_type> clar_list;
    std::map<string, clarity_type> clar_tuple;

    struct option_def{clarity_type* value;}clar_option;
    struct response_def{clarity_type* ok_value; clarity_type* err_value; }clar_response;
};

typedef string clar_string_ascii;
typedef string clar_string_utf8;
typedef vector<clarity_type> clar_list;
typedef std::map<string, clarity_type> clar_tuple;
typedef int64_t clarity_int;
typedef uint64_t clarity_uint;
typedef bool clarity_bool;
typedef string principal;


// hold user account data (deployed contracts, balance in different tokens)
struct account_data
{
    //deployed contracts (as a list of function pointers?)
    //token-balance pairs
};

struct contract_data
{
    principal deployer;
    string contract_name;

    inline string create_contract_principal(){return (deployer + "." + contract_name); }
};

//General blockchain state to provide a fuzzing context
struct BlockchainState
{
    //account states
    unordered_map<principal, account_data> accountData;

    //deployed contracts (we can assume this is immutable inside a fuzzing campaign for now)
    vector<contract_data> contractData;

    //que mas hay en estado que nos sirva?
    //por ejemplo last timestamp, block height, etc.
};


struct ContractEvaluationContext
{
    //TODO: how does the context of a contract work?
    //delta
};


// struct txn
// {
//     //TODO: what are fields of a transaction?
// };