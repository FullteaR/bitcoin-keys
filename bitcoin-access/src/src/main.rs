extern crate bitcoincore_rpc;

use bitcoincore_rpc::{Auth, Client, RpcApi};

fn main() {

    let rpc = Client::new(
        "http://bitcoin-server-main:8332",
        Auth::UserPass("frt".to_string(),
        "pass".to_string())
    ).unwrap();
    
    let block = u64::from(
        rpc.get_mining_info()
            .expect("Failed to fetch the height of latest block")
            .blocks,
    );

    (0..block).into_iter().for_each(|height| {
        if height % 500 == 0 {
            info!("height: {}", height);
        }
        let current_block_hash = match client.get_block_hash(height) {
            Err(_) => {
                error!("leaving, error getting blockhash for height: {} ", height);
                error!("Failed to get block!");
                error!("Is bitcoin daemon running?");
                panic!();
            }
            Ok(h) => h,
        };

        let current_block = client.get_block(&current_block_hash).unwrap();

        current_block.txdata.iter().for_each(|tx| {
            let output_count = tx.output.len();
            tx.input.iter().enumerate().for_each(|(id, input)| {
                let assoc_output = utxos
                    .remove(&(
                        input.previous_output.txid,
                        input.previous_output.vout as usize,
                    ))
                    .unwrap();
                if id < output_count {
                    return;
                }
            
                let sighash_byte = if assoc_output.script_pubkey.is_p2pkh()
                    || assoc_output.script_pubkey.is_p2pk()
                {
                    // p2pk example: d71fd2f64c0b34465b7518d240c00e83f6a5b10138a7079d1252858fe7e6b577
                    //p2pkh example: e03a9a4b5c557f6ee3400a29ff1475d1df73e9cddb48c2391abdc391d8c1504a
                    let sighash_byte =
                        match input.script_sig.instructions().next().unwrap().unwrap() {
                            Instruction::PushBytes(b) => b[b.len() - 1],

                            _ => {
                                return;
                            }
                        };
                    sighash_byte
                } else {
                    return;
                };

                let sighash = match SigHashType::from_u32_standard(sighash_byte as u32) {
                    Err(_) => {
                        return;
                    }
                    Ok(s) => s,
                };
                info!(sighash);
                
            });
        });
    });

}