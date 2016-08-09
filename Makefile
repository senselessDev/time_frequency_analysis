TFTB_SOURCE = http://mirror.easyname.at/nongnu//tftb/tftb-0.2.tar.gz
TMP_DIR := $(shell mktemp -d -t tftb)
TFTB_DIR = tftb-source

$(TFTB_DIR):
	echo $(TMP_DIR)
	wget -P $(TMP_DIR) $(TFTB_SOURCE)
	tar -xf $(addprefix $(TMP_DIR)/, $(notdir $(TFTB_SOURCE))) -C $(TMP_DIR)
	mkdir -p $(TFTB_DIR)
	cp -p $(addprefix $(TMP_DIR)/, $(notdir $(basename $(basename $(TFTB_SOURCE)))))/mfiles/tf* $(TFTB_DIR)

clean:
	rm -rf $(TFTB_DIR)
